"""
DoS & DDoS Attack Classes for AMI-CPSD v2.0.
"""

from typing import List
import numpy as np
import pandas as pd
from attacks.base import Attack


class DoSAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 1

    @property
    def name(self) -> str:
        return "DoS"

    @property
    def domain(self) -> str:
        return "Network"

    @property
    def affected_features(self) -> List[str]:
        return ["packet_rate", "cpu_usage", "ram_usage", "packet_delay", "packet_loss", "queue_length"]

    def apply(
        self,
        df: pd.DataFrame,
        indices: np.ndarray,
        severity: str,
        stage: str,
        rng: np.random.Generator,
    ) -> pd.DataFrame:
        if len(indices) == 0:
            return df
        scale = self.get_severity_scale(severity)
        count = len(indices)

        df.loc[indices, "packet_rate"] = (rng.uniform(150.0, 500.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "cpu_usage"] = np.minimum(99.0, df.loc[indices, "cpu_usage"] + 45.0 * scale).astype(np.float32)
        df.loc[indices, "ram_usage"] = np.minimum(98.0, df.loc[indices, "ram_usage"] + 35.0 * scale).astype(np.float32)
        df.loc[indices, "packet_delay"] = (rng.uniform(80.0, 300.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "queue_length"] = (rng.uniform(50.0, 150.0, size=count) * scale).astype(np.float32)
        return df


class DDoSAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 2

    @property
    def name(self) -> str:
        return "DDoS"

    @property
    def domain(self) -> str:
        return "Network"

    @property
    def affected_features(self) -> List[str]:
        return ["packet_rate", "packet_delay", "packet_loss", "cpu_usage", "ram_usage", "queue_length", "temperature"]

    def apply(
        self,
        df: pd.DataFrame,
        indices: np.ndarray,
        severity: str,
        stage: str,
        rng: np.random.Generator,
    ) -> pd.DataFrame:
        if len(indices) == 0:
            return df
        scale = self.get_severity_scale(severity)
        count = len(indices)

        df.loc[indices, "packet_rate"] = (rng.uniform(1000.0, 5000.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "packet_delay"] = (rng.uniform(500.0, 2500.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "cpu_usage"] = rng.uniform(90.0, 100.0, size=count).astype(np.float32)
        df.loc[indices, "queue_length"] = (rng.uniform(200.0, 1000.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "temperature"] = (df.loc[indices, "temperature"] + 12.0 * scale).astype(np.float32)
        return df
