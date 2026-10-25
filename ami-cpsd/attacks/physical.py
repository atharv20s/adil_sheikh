"""
Physical Layer Attack Classes (FDI, Data Tampering, Insider) for AMI-CPSD v2.0.
"""

from typing import List
import numpy as np
import pandas as pd
from attacks.base import Attack


class FDIAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 5

    @property
    def name(self) -> str:
        return "False Data Injection"

    @property
    def domain(self) -> str:
        return "Physical"

    @property
    def affected_features(self) -> List[str]:
        return ["voltage", "current", "active_power", "energy", "autoencoder_score", "isolation_forest_score"]

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

        v_vals = np.where(
            rng.random(size=count) > 0.5,
            rng.uniform(255.0, 285.0, size=count),
            rng.uniform(160.0, 195.0, size=count),
        )
        df.loc[indices, "voltage"] = v_vals.astype(np.float32)
        df.loc[indices, "active_power"] = (rng.uniform(0.01, 0.2, size=count) if scale > 0.8 else rng.uniform(12.0, 20.0, size=count)).astype(np.float32)
        df.loc[indices, "autoencoder_score"] = np.float32(min(0.99, 0.25 * scale))
        return df


class DataTamperingAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 10

    @property
    def name(self) -> str:
        return "Data Tampering"

    @property
    def domain(self) -> str:
        return "Physical"

    @property
    def affected_features(self) -> List[str]:
        return ["packet_size", "signature_valid", "drift_score", "energy"]

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
        count = len(indices)
        df.loc[indices, "packet_size"] = np.where(rng.random(size=count) > 0.5, 4500.0, 15.0).astype(np.float32)
        df.loc[indices, "signature_valid"] = 0.0
        df.loc[indices, "energy"] = np.where(rng.random(size=count) > 0.5, 99999.0, 0.0).astype(np.float32)
        return df


class InsiderAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 11

    @property
    def name(self) -> str:
        return "Insider Attack"

    @property
    def domain(self) -> str:
        return "Physical"

    @property
    def affected_features(self) -> List[str]:
        return ["active_power", "drift_score", "anomaly_score"]

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
        df.loc[indices, "authentication_success"] = 1.0
        df.loc[indices, "signature_valid"] = 1.0
        df.loc[indices, "active_power"] = (df.loc[indices, "active_power"] * (1.0 - 0.3 * scale)).astype(np.float32)
        return df
