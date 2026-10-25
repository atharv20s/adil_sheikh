"""
Consensus & Blockchain Attack Classes (Sybil, Byzantine, Key Theft) for AMI-CPSD v2.0.
"""

from typing import List
import numpy as np
import pandas as pd
from attacks.base import Attack


class SybilAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 6

    @property
    def name(self) -> str:
        return "Sybil"

    @property
    def domain(self) -> str:
        return "Consensus"

    @property
    def affected_features(self) -> List[str]:
        return ["validator_votes", "leader_change", "entropy", "byzantine_votes", "queue_length"]

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
        df.loc[indices, "validator_votes"] = np.float32(24.0 + 15.0 * scale)
        df.loc[indices, "byzantine_votes"] = rng.poisson(lam=4.0 * scale, size=count).astype(np.float32)
        df.loc[indices, "queue_length"] = (rng.uniform(80.0, 250.0, size=count) * scale).astype(np.float32)
        return df


class ByzantineAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 7

    @property
    def name(self) -> str:
        return "Byzantine"

    @property
    def domain(self) -> str:
        return "Consensus"

    @property
    def affected_features(self) -> List[str]:
        return ["byzantine_votes", "failed_consensus", "leader_change", "consensus_latency", "smart_contract_latency"]

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
        df.loc[indices, "byzantine_votes"] = (rng.uniform(5.0, 14.0, size=count) * scale).astype(np.float32)
        df.loc[indices, "failed_consensus"] = rng.poisson(lam=4.0 * scale, size=count).astype(np.float32)
        df.loc[indices, "consensus_latency"] = (rng.uniform(800.0, 3200.0, size=count) * scale).astype(np.float32)
        return df


class KeyTheftAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 9

    @property
    def name(self) -> str:
        return "Key Theft"

    @property
    def domain(self) -> str:
        return "Consensus"

    @property
    def affected_features(self) -> List[str]:
        return ["tpm_status", "session_duration", "byzantine_votes", "drift_score"]

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
        df.loc[indices, "encryption_enabled"] = 1.0
        df.loc[indices, "signature_valid"] = 1.0
        df.loc[indices, "tpm_status"] = 0.0
        df.loc[indices, "drift_score"] = np.float32(min(0.95, 0.35 * scale))
        return df
