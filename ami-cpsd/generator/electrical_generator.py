"""
Electrical Data Generator (AMI-CPSD v1.0).
Simulates grid physical layer features with continuous Ornstein–Uhlenbeck temporal state evolution
and consumer load profile coupling (Residential, Commercial, Industrial).
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig
from generator.consumer_profiles import ConsumerProfiles
from generator.physics_engine import PhysicsEngine


class ElectricalGenerator:
    """Generates continuous, physics-constrained smart grid electrical measurements."""

    def __init__(self, config: DataConfig):
        self.config = config
        self.consumer_profiles = ConsumerProfiles(config)
        self.physics_engine = PhysicsEngine(config)

    def generate(
        self,
        n_samples: int,
        consumer_types: np.ndarray,
        time_of_day: np.ndarray,
        ambient_temp: np.ndarray,
        rng: np.random.Generator,
    ) -> pd.DataFrame:
        """
        Generates continuous physical electrical measurements.

        :param n_samples: Number of rows.
        :param consumer_types: Array of consumer types ("Residential", "Commercial", "Industrial").
        :param time_of_day: Hour of day array (0.0 to 23.99).
        :param ambient_temp: Ambient temperature array (°C).
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing electrical features.
        """
        dt = 0.25  # 15-minute sampling interval in hours

        # 1. Voltage: Continuous Ornstein-Uhlenbeck process (mean=229V, theta=0.8, sigma=0.6)
        voltage = self.physics_engine.generate_ou_process(
            n_samples=n_samples,
            mean=self.config.nominal_voltage,
            theta=0.8,
            sigma=0.6,
            dt=dt,
            initial_val=self.config.nominal_voltage,
            rng=rng,
        )
        voltage = np.clip(voltage, 215.0, 243.0)

        # 2. Frequency: Continuous OU process (mean=50Hz, theta=1.2, sigma=0.03)
        frequency = self.physics_engine.generate_ou_process(
            n_samples=n_samples,
            mean=self.config.nominal_frequency,
            theta=1.2,
            sigma=0.03,
            dt=dt,
            initial_val=self.config.nominal_frequency,
            rng=rng,
        )
        frequency = np.clip(frequency, 49.7, 50.3)

        # 3. Current: Driven by consumer profiles and ambient temperature
        base_current = np.zeros(n_samples)
        for c_type in ["Residential", "Commercial", "Industrial"]:
            mask = consumer_types == c_type
            if np.any(mask):
                mult = self.consumer_profiles.get_load_multiplier(
                    c_type, time_of_day[mask], ambient_temp[mask], rng
                )
                base_current[mask] = 6.0 * mult

        # Apply continuous OU smoothing to current
        current = self.physics_engine.generate_ou_process(
            n_samples=n_samples,
            mean=float(np.mean(base_current)),
            theta=0.5,
            sigma=1.0,
            dt=dt,
            initial_val=float(base_current[0]),
            rng=rng,
        )
        current = np.clip(np.abs(current) + base_current * 0.5, 1.0, 50.0)

        # 4. Power factor: Beta distribution scaled to [0.88, 0.98]
        power_factor = rng.beta(a=12, b=2, size=n_samples) * 0.11 + 0.88
        power_factor = np.clip(power_factor, 0.80, 0.999)

        # 5. Active Power (kW) = Voltage (V) * Current (A) * Power Factor / 1000
        active_power = (voltage * current * power_factor) / 1000.0

        # Reactive & Apparent Power calculations
        phi = np.arccos(power_factor)
        reactive_power = active_power * np.tan(phi)
        apparent_power = np.sqrt(active_power**2 + reactive_power**2)

        # 6. Cumulative Energy (kWh)
        energy = np.cumsum(active_power * dt) + rng.normal(0, 0.02, size=n_samples)
        energy = np.maximum(energy, 0.0)

        # 7. Peak Demand & Load Variance
        peak_demand = active_power * rng.uniform(1.1, 1.35, size=n_samples)
        load_variance = (active_power * 0.15) ** 2 + rng.exponential(scale=0.02, size=n_samples)

        df = pd.DataFrame(
            {
                "voltage": np.round(voltage, 3),
                "current": np.round(current, 3),
                "frequency": np.round(frequency, 3),
                "active_power": np.round(active_power, 4),
                "reactive_power": np.round(reactive_power, 4),
                "apparent_power": np.round(apparent_power, 4),
                "power_factor": np.round(power_factor, 4),
                "energy": np.round(energy, 4),
                "peak_demand": np.round(peak_demand, 4),
                "load_variance": np.round(load_variance, 5),
            }
        )

        return df
