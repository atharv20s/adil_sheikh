"""
IDS Data Generator.
Simulates Intrusion Detection System metrics (entropy, drift, anomaly scores, baseline ML scores).
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig


class IDSGenerator:
    """Generates synthetic IDS security metrics for smart grid monitoring."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate(self, n_samples: int, rng: np.random.Generator) -> pd.DataFrame:
        """
        Generates baseline IDS metrics for normal traffic.

        :param n_samples: Number of observations.
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing IDS features.
        """
        # Anomaly Score (0.0 - 0.1 baseline): Beta distribution
        anomaly_score = rng.beta(a=1.5, b=25.0, size=n_samples) * 0.15
        anomaly_score = np.clip(anomaly_score, 0.0, 0.2)

        # Network Packet Entropy (bits): Normal distribution 4.0 ± 0.25 (range 3.5 - 4.5)
        entropy = rng.normal(loc=4.0, scale=0.25, size=n_samples)
        entropy = np.clip(entropy, 3.2, 4.8)

        # Packet Diversity Ratio: Beta distribution (range 0.70 - 0.95)
        packet_diversity = rng.beta(a=20.0, b=4.0, size=n_samples) * 0.28 + 0.68
        packet_diversity = np.clip(packet_diversity, 0.60, 0.98)

        # Concept Drift Score (0.0 - 0.1 baseline): Exponential distribution
        drift_score = rng.exponential(scale=0.02, size=n_samples)
        drift_score = np.clip(drift_score, 0.0, 0.15)

        # Isolation Forest Anomaly Score: Normal distribution centered at 0.25 (normal > 0)
        isolation_forest_score = rng.normal(loc=0.25, scale=0.08, size=n_samples)
        isolation_forest_score = np.clip(isolation_forest_score, -0.05, 0.50)

        # Autoencoder Reconstruction Loss: Gamma distribution (range 0.001 - 0.04)
        autoencoder_score = rng.gamma(shape=2.0, scale=0.008, size=n_samples)
        autoencoder_score = np.clip(autoencoder_score, 0.001, 0.08)

        # One-Class SVM Decision Score: Normal distribution centered at +1.2
        svm_score = rng.normal(loc=1.2, scale=0.3, size=n_samples)
        svm_score = np.clip(svm_score, 0.1, 2.5)

        df = pd.DataFrame(
            {
                "anomaly_score": np.round(anomaly_score, 4),
                "entropy": np.round(entropy, 4),
                "packet_diversity": np.round(packet_diversity, 4),
                "drift_score": np.round(drift_score, 4),
                "isolation_forest_score": np.round(isolation_forest_score, 4),
                "autoencoder_score": np.round(autoencoder_score, 5),
                "svm_score": np.round(svm_score, 4),
            }
        )

        return df
