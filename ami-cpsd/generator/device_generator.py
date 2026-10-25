"""
Device Hardware Data Generator.
Simulates smart meter cyber-physical device metrics (CPU, RAM, Temp, Firmware, TPM).
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig


class DeviceGenerator:
    """Generates synthetic hardware telemetry for smart meter endpoints."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate(self, n_samples: int, rng: np.random.Generator) -> pd.DataFrame:
        """
        Generates normal device hardware metrics.

        :param n_samples: Number of observations.
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing device hardware features.
        """
        # CPU Usage (%): Gaussian distribution centered at 27% (range 20-35%)
        cpu_usage = rng.normal(loc=27.0, scale=3.5, size=n_samples)
        cpu_usage = np.clip(cpu_usage, 10.0, 45.0)

        # RAM Usage (%): Gaussian distribution centered at 40% (range 30-50%)
        ram_usage = rng.normal(loc=40.0, scale=4.5, size=n_samples)
        ram_usage = np.clip(ram_usage, 20.0, 60.0)

        # Flash Storage Usage (%): Normal distribution around 55%
        flash_usage = rng.normal(loc=55.0, scale=5.0, size=n_samples)
        flash_usage = np.clip(flash_usage, 25.0, 85.0)

        # Operating Temperature (°C): Normal distribution 38 ± 2.5°C
        temperature = rng.normal(loc=38.0, scale=2.5, size=n_samples)
        temperature = np.clip(temperature, 25.0, 50.0)

        # Battery Health (%): Beta distribution skewed to 95-100%
        battery = 100.0 - rng.beta(a=1, b=8, size=n_samples) * 10.0
        battery = np.clip(battery, 85.0, 100.0)

        # Firmware Hash Integrity: 1 = Valid, 0 = Compromised/Tampered
        firmware_hash_valid = rng.choice([1.0, 0.0], size=n_samples, p=[0.998, 0.002])

        # Reboot Count: Poisson distribution (lambda=0.01)
        reboot_count = rng.poisson(lam=0.01, size=n_samples).astype(float)

        # Secure Boot Status: 1 = Enabled/Verified
        secure_boot = rng.choice([1.0, 0.0], size=n_samples, p=[0.999, 0.001])

        # TPM Status: 1 = Active/Healthy, 0 = Tampered/Error
        tpm_status = rng.choice([1.0, 0.0], size=n_samples, p=[0.999, 0.001])

        df = pd.DataFrame(
            {
                "cpu_usage": np.round(cpu_usage, 2),
                "ram_usage": np.round(ram_usage, 2),
                "flash_usage": np.round(flash_usage, 2),
                "temperature": np.round(temperature, 2),
                "battery": np.round(battery, 2),
                "firmware_hash_valid": firmware_hash_valid,
                "reboot_count": reboot_count,
                "secure_boot": secure_boot,
                "tpm_status": tpm_status,
            }
        )

        return df
