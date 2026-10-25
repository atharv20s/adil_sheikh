"""
Physics Engine for AMI-CPSD v2.0.
Implements continuous Ornstein–Uhlenbeck temporal processes, P = VIcos(phi) validation,
sensor noise modeling, and missing data injection.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


class PhysicsEngine:
    """Core physics modeling & validation engine."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.nominal_voltage = config.get("simulation", {}).get("nominal_voltage", 229.0)
        self.nominal_frequency = config.get("simulation", {}).get("nominal_frequency", 50.0)
        self.missing_data_pct = config.get("simulation", {}).get("missing_data_pct", 0.015)

    def generate_ou_process(
        self,
        n_samples: int,
        mean: float,
        theta: float,
        sigma: float,
        dt: float,
        initial_val: float,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """
        Generates a continuous Ornstein-Uhlenbeck (OU) mean-reverting process.
        """
        x = np.zeros(n_samples, dtype=np.float32)
        x[0] = initial_val
        noise = rng.normal(0.0, 1.0, size=n_samples).astype(np.float32)

        for t in range(1, n_samples):
            dx = theta * (mean - x[t - 1]) * dt + sigma * np.sqrt(dt) * noise[t]
            x[t] = x[t - 1] + dx

        return x

    def apply_feeder_voltage_drop(
        self,
        base_voltage: np.ndarray,
        current: np.ndarray,
        feeder_distance_m: np.ndarray,
        r_per_km: float = 0.4 # Line resistance 0.4 Ohm/km
    ) -> np.ndarray:
        """
        Applies Ohmic line losses and voltage drop along feeder length:
        V_node = V_substation - (I * R_per_km * distance_km)
        """
        r_total = r_per_km * (feeder_distance_m / 1000.0)
        voltage_drop = current * r_total
        return np.clip(base_voltage - voltage_drop, 180.0, 260.0).astype(np.float32)

    def validate_and_correct_power_physics(
        self,
        voltage: np.ndarray,
        current: np.ndarray,
        power_factor: np.ndarray,
        active_power: np.ndarray,
        is_attack: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Validates P_calc = (V * I * pf) / 1000.
        For normal samples (is_attack == 0), guarantees physical exactness.
        """
        p_calc = (voltage * current * power_factor) / 1000.0
        normal_mask = is_attack == 0
        active_power = np.where(normal_mask, p_calc, active_power)

        phi = np.arccos(np.clip(power_factor, 0.5, 1.0))
        reactive_power = active_power * np.tan(phi)
        apparent_power = np.sqrt(active_power**2 + reactive_power**2)

        return active_power.astype(np.float32), reactive_power.astype(np.float32), apparent_power.astype(np.float32)

    def add_sensor_noise(
        self, df: pd.DataFrame, rng: np.random.Generator
    ) -> pd.DataFrame:
        """Injects ADC quantization noise, calibration bias, and jitter."""
        df = df.copy()
        n = len(df)

        if "voltage" in df.columns:
            df["voltage"] += rng.normal(0.0, 0.05, size=n).astype(np.float32)
        if "temperature" in df.columns:
            df["temperature"] += rng.normal(0.0, 0.1, size=n).astype(np.float32)
        if "packet_delay" in df.columns:
            df["packet_delay"] += rng.normal(0.0, 0.5, size=n).astype(np.float32)
            df["packet_delay"] = np.maximum(df["packet_delay"], 0.5)

        return df

    def inject_missing_data(
        self, df: pd.DataFrame, rng: np.random.Generator
    ) -> pd.DataFrame:
        """Injects 1-3% NaN values into communication & device telemetry columns."""
        df = df.copy()
        n = len(df)
        pct = self.missing_data_pct

        target_cols = [
            "packet_delay", "packet_loss", "rssi", "cpu_usage",
            "ram_usage", "temperature", "consensus_latency", "drift_score"
        ]

        for col in target_cols:
            if col in df.columns:
                mask = rng.random(size=n) < pct
                df.loc[mask, col] = np.nan

        return df
