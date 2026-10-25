"""
Blockchain Data Generator (AMI-CPSD v1.0).
Simulates multi-consensus Byzantine Fault Tolerant (BFT) protocols: PBFT, IBFT, QBFT, TowerBFT, RVR_BFT.
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig, CONSENSUS_PROTOCOLS


class BlockchainGenerator:
    """Generates multi-protocol consensus telemetry."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate(
        self, n_samples: int, protocols: np.ndarray, rng: np.random.Generator
    ) -> pd.DataFrame:
        """
        Generates consensus telemetry adjusted by BFT protocol parameters.

        :param n_samples: Number of observations.
        :param protocols: Array of protocol names ("PBFT", "IBFT", "QBFT", "TowerBFT", "RVR_BFT").
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing blockchain features.
        """
        consensus_latency = np.zeros(n_samples)
        transaction_delay = np.zeros(n_samples)
        validator_votes = np.zeros(n_samples)
        block_interval = np.zeros(n_samples)
        smart_contract_latency = np.zeros(n_samples)

        # Base generation tailored by BFT protocol characteristics
        for proto in CONSENSUS_PROTOCOLS:
            mask = protocols == proto
            count = np.sum(mask)
            if count == 0:
                continue

            if proto == "PBFT":
                consensus_latency[mask] = rng.lognormal(mean=5.2, sigma=0.2, size=count)  # ~180 ms
                block_interval[mask] = rng.normal(2.0, 0.1, size=count)
                validator_votes[mask] = 16.0
            elif proto == "IBFT":
                consensus_latency[mask] = rng.lognormal(mean=5.0, sigma=0.2, size=count)  # ~150 ms
                block_interval[mask] = rng.normal(1.8, 0.08, size=count)
                validator_votes[mask] = 16.0
            elif proto == "QBFT":
                consensus_latency[mask] = rng.lognormal(mean=4.8, sigma=0.18, size=count)  # ~120 ms
                block_interval[mask] = rng.normal(1.5, 0.05, size=count)
                validator_votes[mask] = 16.0
            elif proto == "TowerBFT":
                # High-speed Solana style TowerBFT
                consensus_latency[mask] = rng.lognormal(mean=3.9, sigma=0.15, size=count)  # ~50 ms
                block_interval[mask] = rng.normal(0.4, 0.02, size=count)
                validator_votes[mask] = 32.0
            elif proto == "RVR_BFT":
                # Verifiable Random BFT (IEEE TPDS 2025)
                consensus_latency[mask] = rng.lognormal(mean=4.3, sigma=0.15, size=count)  # ~75 ms
                block_interval[mask] = rng.normal(0.8, 0.04, size=count)
                validator_votes[mask] = 24.0

            transaction_delay[mask] = rng.exponential(scale=15.0, size=count)
            smart_contract_latency[mask] = rng.lognormal(mean=3.0, sigma=0.25, size=count)

        consensus_latency = np.clip(consensus_latency, 30.0, 500.0)
        transaction_delay = np.clip(transaction_delay, 5.0, 150.0)
        block_interval = np.clip(block_interval, 0.3, 3.0)
        smart_contract_latency = np.clip(smart_contract_latency, 5.0, 100.0)

        failed_consensus = rng.poisson(lam=0.005, size=n_samples).astype(float)
        leader_change = rng.poisson(lam=0.01, size=n_samples).astype(float)
        queue_length = rng.poisson(lam=15.0, size=n_samples).astype(float)
        byzantine_votes = rng.poisson(lam=0.002, size=n_samples).astype(float)

        df = pd.DataFrame(
            {
                "consensus_latency": np.round(consensus_latency, 2),
                "transaction_delay": np.round(transaction_delay, 2),
                "validator_votes": validator_votes,
                "failed_consensus": failed_consensus,
                "block_interval": np.round(block_interval, 3),
                "leader_change": leader_change,
                "queue_length": queue_length,
                "smart_contract_latency": np.round(smart_contract_latency, 2),
                "byzantine_votes": byzantine_votes,
            }
        )

        return df
