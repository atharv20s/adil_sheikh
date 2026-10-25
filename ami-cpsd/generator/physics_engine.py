"""
Physics Engine for AMI-CPSD v1.0.
Implements Ornstein–Uhlenbeck temporal processes, physical power constraints (P = VIcos(phi)),
sensor noise modeling, and missing data injection.
"""

import numpy as np
import pandas as pd
from typing import Tuple
from generator.config import DataConfig


class PhysicsEngine:
    """Core physical modeling & validation engine."""

    def __init__(self, config: DataConfig):
        self.config = config

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
        Generates a continuous Ornstein-Uhlenbeck (OU) mean-reverting time series.
        x_t = x_{t-1} + theta * (mean - x_{t-1}) * dt + sigma * sqrt(dt) * N(0, 1)

        :return: Array of continuous state values.
        """
        x = np.zeros(n_samples)
        x[0] = initial_val
        noise = rng.normal(0.0, 1.0, size=n_samples)

        for t in range(1, n_samples):
            dx = theta * (mean - x[t - 1]) * dt + sigma * np.sqrt(dt) * noise[t]
            x[t] = x[t - 1] + dx

        return x

    def validate_and_correct_power_physics(
        self,
        voltage: np.ndarray,
        current: np.ndarray,
        power_factor: np.ndarray,
        active_power: np.ndarray,
        is_attack: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Validates electrical active power physics P_calc = (V * I * pf) / 1000.
        For normal samples (is_attack == 0), guarantees |P_calc - P_measured| < tolerance.

        :return: Tuple of (validated_active_power, reactive_power, apparent_power)
        """
        p_calc = (voltage * current * power_factor) / 1000.0

        # For normal traffic, enforce exact physics matching
        normal_mask = is_attack == 0
        active_power = np.where(normal_mask, p_calc, active_power)

        # Re-compute reactive & apparent power based on valid active power
        phi = np.arccos(np.clip(power_factor, 0.5, 1.0))
        reactive_power = active_power * np.tan(phi)
        apparent_power = np.sqrt(active_power**2 + reactive_power**2)

        return active_power, reactive_power, apparent_power

    def add_sensor_noise(
        self, df: pd.DataFrame, rng: np.random.Generator
    ) -> pd.DataFrame:
        """
        Injects realistic analog-to-digital (ADC) noise, calibration bias, and jitter.
        """
        df = df.copy()
        n = len(df)

        # ADC Voltage quantization noise (±0.05V)
        if "voltage" in df.columns:
            df["voltage"] += rng.normal(0.0, 0.05, size=n)

        # Temperature sensor thermal jitter (±0.1°C)
        if "temperature" in df.columns:
            df["temperature"] += rng.normal(0.0, 0.1, size=n)

        # Packet Delay Network Jitter (±0.5ms)
        if "packet_delay" in df.columns:
            df["packet_delay"] += rng.normal(0.0, 0.5, size=n)
            df["packet_delay"] = np.maximum(df["packet_delay"], 0.5)

        return df

    def inject_missing_data(
        self, df: pd.DataFrame, rng: np.random.Generator
    ) -> pd.DataFrame:
        """
        Injects 1-3% NaN values into communication & device telemetry columns.
        """
        df = df.copy()
        n = len(df)
        pct = self.config.missing_data_pct

        target_cols = [
            "packet_delay",
            "packet_loss",
            "rssi",
            "cpu_usage",
            "ram_usage",
            "temperature",
            "consensus_latency",
            "drift_score",
        ]

        for col in target_cols:
            if col in df.columns:
                mask = rng.random(size=n) < pct
                df.loc[mask, col] = np.nan

        return df
