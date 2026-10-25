"""
AMI-CPSD v3.0 Event-Driven Simulation Kernel Architecture.
Central orchestrator managing causal feedback step loops across weather, 
physics, meter states, FSM attack transitions, consensus feedback, and telemetry exporters.
"""

import time
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from pathlib import Path

from simulator.weather import WeatherGenerator
from simulator.physics import PhysicsEngine
from simulator.profiles import ConsumerProfiles
from simulator.meter_state import PersistentMeterEngine
from simulator.fsm import MeterFSM, AttackStageFSM
from simulator.consensus import ClosedLoopConsensusEngine
from attacks.registry import AttackRegistry

logger = logging.getLogger(__name__)


class SimulationKernel:
    """Master Event-Driven Digital Twin Simulation Kernel."""
    def __init__(self, config: Dict[str, Any], topology_data: Dict[str, Any]):
        self.config = config
        self.topology_data = topology_data
        self.physics = PhysicsEngine(config)
        self.weather_gen = WeatherGenerator(config)
        self.profiles = ConsumerProfiles(config)
        
        meter_map = topology_data["meter_assignments"]
        self.meter_ids = list(meter_map.keys())
        self.num_meters = len(self.meter_ids)

        self.meter_engine = PersistentMeterEngine(num_meters=self.num_meters)
        self.consensus_engine = ClosedLoopConsensusEngine(num_nodes=self.num_meters)
        self.attack_registry = AttackRegistry()
        
        # Instantiate FSM state machines per meter
        self.fsm_map: Dict[str, MeterFSM] = {mid: MeterFSM(mid) for mid in self.meter_ids}

    def run_step(self, tick: int, rng: np.random.Generator, is_zero_day: bool = False) -> pd.DataFrame:
        """
        Executes a single simulation tick in causal order:
        1. Weather update
        2. Meter states OU step & profile load
        3. Feeder physics & voltage drop
        4. FSM attack lifecycle transition
        5. Consensus feedback loop (Byzantine -> latency -> queue backlog -> delay)
        6. Feature perturbation via pluggable Attack Registry
        7. Combined observation dataframe snapshot
        """
        # 1. Weather Update
        time_offset_hours = (tick * 15 * 60) / 3600.0
        df_weather = self.weather_gen.generate(self.num_meters, np.full(self.num_meters, time_offset_hours), rng)
        timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(1767225600 + tick * 15 * 60))

        # 2. Meter States Step
        self.meter_engine.step_all(dt=1.0)
        base_v = np.array([self.meter_engine.get_state(m).voltage for m in self.meter_ids], dtype=np.float32)
        base_i = np.array([self.meter_engine.get_state(m).current for m in self.meter_ids], dtype=np.float32)
        base_pf = np.array([self.meter_engine.get_state(m).power_factor for m in self.meter_ids], dtype=np.float32)
        distances = np.array([self.meter_engine.get_state(m).feeder_distance_m for m in self.meter_ids], dtype=np.float32)
        consumer_types = [self.meter_engine.get_state(m).profile for m in self.meter_ids]

        # 3. Feeder Voltage Drop & Power Physics
        voltage = self.physics.apply_feeder_voltage_drop(base_v, base_i, distances)
        frequency = np.clip(50.0 + rng.normal(0, 0.02, size=self.num_meters), 49.7, 50.3).astype(np.float32)
        active_power = (voltage * base_i * base_pf) / 1000.0
        phi = np.arccos(base_pf)
        reactive_power = active_power * np.tan(phi)
        apparent_power = np.sqrt(active_power**2 + reactive_power**2)

        # Monotonic Cumulative Energy per meter
        energy = np.cumsum(active_power * 0.25).astype(np.float32)

        # 4. FSM Attack LifeCycle
        attack_types = []
        attack_stages = []
        is_attack = []

        attack_map_names = {
            0: "Normal", 1: "DoS", 2: "DDoS", 3: "Replay", 4: "MITM", 5: "False Data Injection",
            6: "Sybil", 7: "Byzantine", 8: "Firmware Attack", 9: "Key Theft", 10: "Data Tampering",
            11: "Insider Attack", 12: "Malware"
        }

        for mid in self.meter_ids:
            fsm = self.fsm_map[mid]
            # Randomly trigger attack if normal
            if fsm.state == AttackStageFSM.NORMAL and rng.random() < 0.08:
                a_id = int(rng.choice([8, 11, 12] if is_zero_day else [1, 2, 3, 4, 5, 6, 7, 9, 10]))
                fsm.trigger_attack(a_id)
            
            curr_state = fsm.step(rng)
            a_type = fsm.target_attack_type if curr_state != AttackStageFSM.NORMAL else 0
            attack_types.append(a_type)
            attack_stages.append(fsm.get_stage_name())
            is_attack.append(1 if a_type != 0 else 0)

        attack_types_arr = np.array(attack_types, dtype=np.int32)
        byzantine_votes = np.where(attack_types_arr == 7, rng.uniform(5.0, 14.0, size=self.num_meters), 0.0).astype(np.float32)
        failed_consensus = np.where(attack_types_arr == 7, rng.poisson(4.0, size=self.num_meters), 0.0).astype(np.float32)
        base_delay = np.clip(rng.lognormal(2.3, 0.3, size=self.num_meters), 3.0, 50.0).astype(np.float32)

        # 5. Closed-Loop Consensus Feedback
        c_lat, q_len, eff_delay, p_loss = self.consensus_engine.step(byzantine_votes, failed_consensus, base_delay, rng)

        # 6. Build Snapshot DataFrame
        df_step = pd.DataFrame({
            "timestamp": [timestamp_str] * self.num_meters,
            "meter_id": self.meter_ids,
            "substation_id": [self.topology_data["meter_assignments"][m]["substation_id"] for m in self.meter_ids],
            "feeder_id": [self.topology_data["meter_assignments"][m]["feeder_id"] for m in self.meter_ids],
            "transformer_id": [self.topology_data["meter_assignments"][m]["transformer_id"] for m in self.meter_ids],
            "nan_id": [self.topology_data["meter_assignments"][m]["nan_id"] for m in self.meter_ids],
            "dc_id": [self.topology_data["meter_assignments"][m]["dc_id"] for m in self.meter_ids],
            "validator_group": [f"VAL_GRP-{(i%8)+1:02d}" for i in range(self.num_meters)],
            "location": [f"Zone_{m[3:]}" for m in self.meter_ids],
            "consumer_type": consumer_types,
            "grid_state": ["Normal"] * self.num_meters,
            "consensus_protocol": ["TowerBFT"] * self.num_meters,
            "ambient_temperature": df_weather["ambient_temperature"].values,
            "humidity": df_weather["humidity"].values,
            "solar_irradiance": df_weather["solar_irradiance"].values,
            "wind_speed": df_weather["wind_speed"].values,
            "time_of_day": df_weather["time_of_day"].values,
            "day_of_week": df_weather["day_of_week"].values,
            "is_holiday": df_weather["is_holiday"].values,
            "voltage": np.round(voltage, 3),
            "current": np.round(base_i, 3),
            "frequency": np.round(frequency, 3),
            "active_power": np.round(active_power, 4),
            "reactive_power": np.round(reactive_power, 4),
            "apparent_power": np.round(apparent_power, 4),
            "power_factor": np.round(base_pf, 4),
            "energy": np.round(energy, 4),
            "peak_demand": np.round(active_power * 1.2, 4),
            "load_variance": np.round((active_power * 0.15)**2, 5),
            "packet_rate": np.round(15.0 + q_len * 0.5, 2),
            "packet_size": np.round(256.0 + q_len * 2.0, 2),
            "packet_delay": np.round(eff_delay, 3),
            "packet_loss": np.round(p_loss, 4),
            "retransmissions": np.round(p_loss * 0.2, 2),
            "rssi": -70.0,
            "encryption_enabled": 1.0,
            "authentication_success": 1.0,
            "signature_valid": 1.0,
            "session_duration": 3600.0,
            "cpu_usage": np.round(15.0 + q_len * 0.2, 2),
            "ram_usage": 40.0,
            "flash_usage": 55.0,
            "temperature": np.round(38.0 + q_len * 0.05, 2),
            "battery": 98.0,
            "firmware_hash_valid": 1.0,
            "reboot_count": 0.0,
            "secure_boot": 1.0,
            "tpm_status": 1.0,
            "consensus_latency": np.round(c_lat, 2),
            "transaction_delay": np.round(c_lat * 0.2, 2),
            "validator_votes": 16.0,
            "failed_consensus": failed_consensus,
            "block_interval": 2.0,
            "leader_change": 0.0,
            "queue_length": q_len,
            "smart_contract_latency": 12.0,
            "byzantine_votes": byzantine_votes,
            "anomaly_score": 0.05,
            "entropy": 4.0,
            "packet_diversity": 0.85,
            "drift_score": 0.02,
            "isolation_forest_score": 0.25,
            "autoencoder_score": 0.01,
            "svm_score": 1.2,
            "attack_type": attack_types_arr,
            "attack_category": [attack_map_names[a] for a in attack_types_arr],
            "is_attack": is_attack,
            "attack_domain": ["Cyber" if a!=0 else "Normal" for a in attack_types_arr],
            "attack_severity": ["Medium" if a!=0 else "None" for a in attack_types_arr],
            "attack_stage": attack_stages,
            "affected_features": ["voltage" if a!=0 else "" for a in attack_types_arr],
            "attack_start": [timestamp_str if a!=0 else "" for a in attack_types_arr],
            "attack_end": [timestamp_str if a!=0 else "" for a in attack_types_arr],
            "duration_sec": [900.0 if a!=0 else 0.0 for a in attack_types_arr],
            "recovery_time_sec": [300.0 if a!=0 else 0.0 for a in attack_types_arr]
        })

        # 7. Apply Feature Perturbations from Attack Registry
        for a_id in range(1, 13):
            idx = np.where(attack_types_arr == a_id)[0]
            if len(idx) > 0:
                attack_obj = self.attack_registry.get_attack(a_id)
                df_step = attack_obj.apply(df_step, idx, severity="Medium", stage="Impact", rng=rng)

        # 8. Re-validate Power Physics Residuals
        v_act, r_act, a_act = self.physics.validate_and_correct_power_physics(
            df_step["voltage"].values, df_step["current"].values, df_step["power_factor"].values, df_step["active_power"].values, df_step["is_attack"].values
        )
        df_step["active_power"] = np.round(v_act, 4)
        df_step["reactive_power"] = np.round(r_act, 4)
        df_step["apparent_power"] = np.round(a_act, 4)

        return df_step


if __name__ == "__main__":
    from simulator.topology import TopologyGenerator
    cfg = {"simulation": {"nominal_voltage": 230.0, "nominal_frequency": 50.0}, "seeds": {"train_seed": 42}}
    topo = TopologyGenerator(cfg).export_graph_files(Path("datasets"), np.random.default_rng(42))
    kernel = SimulationKernel(cfg, topo)
    df_out = kernel.run_step(tick=1, rng=np.random.default_rng(42))
    print(f"SimulationKernel successfully executed step. Output shape: {df_out.shape}")
