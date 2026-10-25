"""
Network Attack Classes (Replay, MITM) for AMI-CPSD v2.0.
"""

from typing import List
import numpy as np
import pandas as pd
from attacks.base import Attack


class ReplayAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 3

    @property
    def name(self) -> str:
        return "Replay"

    @property
    def domain(self) -> str:
        return "Network"

    @property
    def affected_features(self) -> List[str]:
        return ["retransmissions", "drift_score", "packet_diversity", "entropy", "isolation_forest_score"]

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
        df.loc[indices, "retransmissions"] = (rng.uniform(10.0, 50.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "signature_valid"] = 1.0
        df.loc[indices, "drift_score"] = np.minimum(0.99, 0.4 + 0.5 * scale).astype(np.float32)
        df.loc[indices, "entropy"] = np.maximum(1.2, 4.0 - 1.8 * scale).astype(np.float32)
        return df


class MITMAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return "MITM"

    @property
    def domain(self) -> str:
        return "Network"

    @property
    def affected_features(self) -> List[str]:
        return ["packet_delay", "signature_valid", "authentication_success", "packet_diversity", "svm_score"]

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
        df.loc[indices, "packet_delay"] = (rng.uniform(100.0, 500.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "signature_valid"] = np.where(rng.random(size=count) < 0.75, 0.0, 1.0).astype(np.float32)
        df.loc[indices, "authentication_success"] = np.where(rng.random(size=count) < 0.60, 0.0, 1.0).astype(np.float32)
        return df
