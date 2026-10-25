"""
Abstract Base Attack Class for AMI-CPSD v2.0 Pluggable Attack Engine.
"""

from abc import ABC, abstractmethod
from typing import List
import numpy as np
import pandas as pd


class Attack(ABC):
    """Abstract Base Class for all Cyber-Physical and Network Attacks."""

    @property
    @abstractmethod
    def attack_id(self) -> int:
        """Returns integer attack class ID (0 to 12)."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns string name of the attack."""
        pass

    @property
    @abstractmethod
    def domain(self) -> str:
        """Returns attack domain ('Physical', 'Network', 'Device', 'Consensus')."""
        pass

    @property
    @abstractmethod
    def affected_features(self) -> List[str]:
        """Returns ground-truth list of affected feature names for XAI."""
        pass

    @abstractmethod
    def apply(
        self,
        df: pd.DataFrame,
        indices: np.ndarray,
        severity: str,
        stage: str,
        rng: np.random.Generator,
    ) -> pd.DataFrame:
        """
        Applies attack perturbations to specified DataFrame indices.

        :param df: Target DataFrame chunk.
        :param indices: Array of row indices to perturb.
        :param severity: "Low", "Medium", or "High".
        :param stage: "Reconnaissance", "Exploitation", "Escalation", "Impact", "Post_Attack".
        :param rng: NumPy Random Generator instance.
        :return: Perturbed DataFrame chunk.
        """
        pass

    def get_severity_scale(self, severity: str) -> float:
        """Maps severity string to scaling factor."""
        scales = {"Low": 0.5, "Medium": 1.0, "High": 1.8}
        return scales.get(severity, 1.0)
