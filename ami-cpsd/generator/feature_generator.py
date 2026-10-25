"""
Master Feature Generator for AMI-CPSD v1.0.
Orchestrates digital twin simulation incorporating grid topology, weather, consumer profiles,
physics validation, multi-consensus protocols, attack progression, and sensor noise.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

from generator.config import (
    DataConfig,
    ALL_ENGINEERED_FEATURES,
    METADATA_FEATURES,
    WEATHER_FEATURES,
    ELECTRICAL_FEATURES,
    COMMUNICATION_FEATURES,
    DEVICE_FEATURES,
    BLOCKCHAIN_FEATURES,
    IDS_FEATURES,
    TARGET_LABEL_COLUMNS,
    CONSENSUS_PROTOCOLS,
    GRID_STATES,
)
from generator.topology_generator import TopologyGenerator
from generator.weather_generator import WeatherGenerator
from generator.electrical_generator import ElectricalGenerator
from generator.network_generator import NetworkGenerator
from generator.device_generator import DeviceGenerator
from generator.blockchain_generator import BlockchainGenerator
from generator.ids_generator import IDSGenerator
from generator.label_generator import LabelGenerator
from generator.attack_injector import AttackInjector
from generator.physics_engine import PhysicsEngine


class FeatureGenerator:
    """Master synthesizer bringing together all 19 research-grade digital twin capabilities."""

    def __init__(self, config: DataConfig):
        self.config = config
        self.topology_gen = TopologyGenerator(config)
        self.weather_gen = WeatherGenerator(config)
        self.electrical_gen = ElectricalGenerator(config)
        self.network_gen = NetworkGenerator(config)
        self.device_gen = DeviceGenerator(config)
        self.blockchain_gen = BlockchainGenerator(config)
        self.ids_gen = IDSGenerator(config)
        self.label_gen = LabelGenerator(config)
        self.attack_inj = AttackInjector(config)
        self.physics_engine = PhysicsEngine(config)

    def generate_dataset_split(
        self, n_samples: int, seed: int, is_zero_day_split: bool = False
    ) -> pd.DataFrame:
        """
        Generates a complete digital twin dataset split.

        :param n_samples: Number of observations.
        :param seed: Random seed.
        :param is_zero_day_split: Whether this is the zero_day_test split.
        :return: Consolidated DataFrame.
        """
        rng = np.random.default_rng(seed)

        # 1. Topology & Metadata Setup
        topo_data = self.topology_gen.build_topology(rng)
        meter_map = topo_data["meter_assignments"]
        meter_ids_keys = list(meter_map.keys())

        # Select meter IDs sequentially to simulate time series per meter
        meter_indices = rng.integers(0, len(meter_ids_keys), size=n_samples)
        meter_ids = [meter_ids_keys[i] for i in meter_indices]

        substations = [meter_map[m]["substation_id"] for m in meter_ids]
        feeders = [meter_map[m]["feeder_id"] for m in meter_ids]
        transformers = [meter_map[m]["transformer_id"] for m in meter_ids]
        nans = [meter_map[m]["nan_id"] for m in meter_ids]
        dcs = [meter_map[m]["dc_id"] for m in meter_ids]

        # Timestamps
        start_date = datetime(2026, 1, 1, 0, 0, 0)
        time_offsets_sec = np.sort(rng.integers(0, 30 * 24 * 4, size=n_samples)) * 15 * 60
        time_offsets_hours = time_offsets_sec / 3600.0
        timestamps = [
            (start_date + timedelta(seconds=int(offset))).strftime("%Y-%m-%dT%H:%M:%S")
            for offset in time_offsets_sec
        ]

        val_grp_indices = rng.integers(1, self.config.num_validator_groups + 1, size=n_samples)
        validator_groups = [f"VAL_GRP-{idx:02d}" for idx in val_grp_indices]
        locations = [f"Zone_{m[3:]}" for m in meter_ids]

        # Consumer Profiles & Grid States & BFT Protocols
        c_types = np.array(["Residential", "Commercial", "Industrial"])
        consumer_types = rng.choice(c_types, size=n_samples, p=[0.60, 0.25, 0.15])
        grid_states = rng.choice(GRID_STATES, size=n_samples, p=[0.75, 0.10, 0.05, 0.05, 0.05])
        consensus_protocols = rng.choice(
            CONSENSUS_PROTOCOLS, size=n_samples, p=[0.30, 0.20, 0.20, 0.15, 0.15]
        )

        df_meta = pd.DataFrame(
            {
                "timestamp": timestamps,
                "meter_id": meter_ids,
                "substation_id": substations,
                "feeder_id": feeders,
                "transformer_id": transformers,
                "nan_id": nans,
                "dc_id": dcs,
                "validator_group": validator_groups,
                "location": locations,
                "consumer_type": consumer_types,
                "grid_state": grid_states,
                "consensus_protocol": consensus_protocols,
            }
        )

        # 2. Weather Generation
        df_weather = self.weather_gen.generate(n_samples, time_offsets_hours, rng)

        # 3. Domain Telemetry Generation
        df_elec = self.electrical_gen.generate(
            n_samples,
            consumer_types,
            df_weather["time_of_day"].values,
            df_weather["ambient_temperature"].values,
            rng,
        )
        df_net = self.network_gen.generate(n_samples, rng)
        df_dev = self.device_gen.generate(n_samples, rng)
        df_bc = self.blockchain_gen.generate(n_samples, consensus_protocols, rng)
        df_ids = self.ids_gen.generate(n_samples, rng)

        df = pd.concat([df_meta, df_weather, df_elec, df_net, df_dev, df_bc, df_ids], axis=1)

        # 4. Attack Generation & Multitask Labels
        attack_types, attack_categories, is_attack = self.label_gen.generate_labels(
            n_samples, is_zero_day_split, rng
        )

        df["attack_type"] = attack_types
        df["attack_category"] = attack_categories
        df["is_attack"] = is_attack

        # Inject Attacks & get hierarchical metadata
        (
            df,
            attack_domains,
            attack_severities,
            attack_stages,
            affected_features_list,
        ) = self.attack_inj.inject_attacks(df, attack_types, rng)

        df["attack_domain"] = attack_domains
        df["attack_severity"] = attack_severities
        df["attack_stage"] = attack_stages
        df["affected_features"] = affected_features_list

        # 5. Physics Validation & Sensor Noise
        v_act, r_act, a_act = self.physics_engine.validate_and_correct_power_physics(
            df["voltage"].values,
            df["current"].values,
            df["power_factor"].values,
            df["active_power"].values,
            df["is_attack"].values,
        )
        df["active_power"] = np.round(v_act, 4)
        df["reactive_power"] = np.round(r_act, 4)
        df["apparent_power"] = np.round(a_act, 4)

        df = self.physics_engine.add_sensor_noise(df, rng)

        # 6. Inject Missing Data (1.5% NaNs)
        df = self.physics_engine.inject_missing_data(df, rng)

        # Column Ordering
        all_ordered_columns = (
            METADATA_FEATURES
            + WEATHER_FEATURES
            + ELECTRICAL_FEATURES
            + COMMUNICATION_FEATURES
            + DEVICE_FEATURES
            + BLOCKCHAIN_FEATURES
            + IDS_FEATURES
            + TARGET_LABEL_COLUMNS
        )

        return df[all_ordered_columns]
