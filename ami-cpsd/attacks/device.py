"""
Device Layer Attack Classes (Firmware, Malware) for AMI-CPSD v2.0.
"""

from typing import List
import numpy as np
import pandas as pd
from attacks.base import Attack


class FirmwareAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Firmware Attack"

    @property
    def domain(self) -> str:
        return "Device"

    @property
    def affected_features(self) -> List[str]:
        return ["firmware_hash_valid", "secure_boot", "reboot_count", "cpu_usage", "temperature", "tpm_status"]

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
        df.loc[indices, "firmware_hash_valid"] = 0.0
        df.loc[indices, "secure_boot"] = 0.0
        df.loc[indices, "tpm_status"] = 0.0
        df.loc[indices, "reboot_count"] = (rng.uniform(5.0, 25.0, size=count) * scale).astype(np.float32)
        return df


class MalwareAttack(Attack):
    @property
    def attack_id(self) -> int:
        return 12

    @property
    def name(self) -> str:
        return "Malware"

    @property
    def domain(self) -> str:
        return "Device"

    @property
    def affected_features(self) -> List[str]:
        return ["cpu_usage", "ram_usage", "flash_usage", "temperature", "reboot_count", "entropy"]

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
        df.loc[indices, "cpu_usage"] = np.float32(min(99.0, 85.0 * scale))
        df.loc[indices, "ram_usage"] = np.float32(min(99.0, 90.0 * scale))
        df.loc[indices, "flash_usage"] = np.float32(min(99.0, 92.0 * scale))
        df.loc[indices, "temperature"] = (df.loc[indices, "temperature"] + 15.0 * scale).astype(np.float32)
        return df
