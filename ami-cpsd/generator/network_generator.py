"""
Communication Data Generator.
Simulates network layer statistics for Advanced Metering Infrastructure (AMI).
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig


class NetworkGenerator:
    """Generates synthetic network telemetry for smart meters."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate(self, n_samples: int, rng: np.random.Generator) -> pd.DataFrame:
        """
        Generates normal communication features.

        :param n_samples: Number of observations to generate.
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing network features.
        """
        # Packet rate (pps): Poisson distribution centered at 12 pps
        packet_rate = rng.poisson(lam=12.0, size=n_samples).astype(float)
        packet_rate = np.maximum(packet_rate, 1.0)

        # Packet size (bytes): Normal distribution around 256 bytes
        packet_size = rng.normal(loc=256.0, scale=40.0, size=n_samples)
        packet_size = np.clip(packet_size, 64.0, 1500.0)

        # Packet delay (ms): Log-normal distribution (5-20 ms baseline)
        packet_delay = rng.lognormal(mean=2.3, sigma=0.3, size=n_samples)
        packet_delay = np.clip(packet_delay, 3.0, 50.0)

        # Packet loss (%): Exponential distribution (~0.5% average)
        packet_loss = rng.exponential(scale=0.5, size=n_samples)
        packet_loss = np.clip(packet_loss, 0.0, 5.0)

        # Retransmissions: Poisson distribution (lambda=0.08)
        retransmissions = rng.poisson(lam=0.08, size=n_samples).astype(float)

        # RSSI (dBm): Received Signal Strength Indicator (-70 ± 8 dBm)
        rssi = rng.normal(loc=-70.0, scale=8.0, size=n_samples)
        rssi = np.clip(rssi, -110.0, -40.0)

        # Security state flags
        # encryption_enabled: 1 (active encryption)
        encryption_enabled = rng.choice([1.0, 0.0], size=n_samples, p=[0.99, 0.01])

        # authentication_success: 1 (success)
        authentication_success = rng.choice([1.0, 0.0], size=n_samples, p=[0.995, 0.005])

        # signature_valid: 1 (valid ECC/RSA signature)
        signature_valid = rng.choice([1.0, 0.0], size=n_samples, p=[0.995, 0.005])

        # Session duration (seconds): Log-normal distribution
        session_duration = rng.lognormal(mean=7.5, sigma=0.8, size=n_samples)
        session_duration = np.clip(session_duration, 60.0, 86400.0)

        df = pd.DataFrame(
            {
                "packet_rate": np.round(packet_rate, 2),
                "packet_size": np.round(packet_size, 2),
                "packet_delay": np.round(packet_delay, 3),
                "packet_loss": np.round(packet_loss, 4),
                "retransmissions": np.round(retransmissions, 2),
                "rssi": np.round(rssi, 2),
                "encryption_enabled": encryption_enabled,
                "authentication_success": authentication_success,
                "signature_valid": signature_valid,
                "session_duration": np.round(session_duration, 2),
            }
        )

        return df
