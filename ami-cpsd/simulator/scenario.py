"""
Scenario Engine for AMI-CPSD v2.0.
Defines reusable digital twin simulation scenario configurations.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Scenario:
    """Encapsulates environment, consumer behavior, attack, and blockchain protocol parameters."""

    name: str = "default_summer_peak"
    weather: str = "summer"  # "summer", "winter", "spring", "autumn"
    consumer_profile: str = "mixed"  # "residential", "commercial", "industrial", "mixed"
    attack_mode: str = "standard"  # "standard", "zero_day", "none"
    grid_mode: str = "Normal"  # "Normal", "Peak_Demand", "Grid_Fault", "Maintenance", "Emergency"
    protocol: str = "PBFT"  # "PBFT", "IBFT", "QBFT", "TowerBFT", "RVR_BFT"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "weather": self.weather,
            "consumer_profile": self.consumer_profile,
            "attack_mode": self.attack_mode,
            "grid_mode": self.grid_mode,
            "protocol": self.protocol,
        }
