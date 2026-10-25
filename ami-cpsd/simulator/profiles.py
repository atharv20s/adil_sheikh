"""
Consumer Load Profiles for AMI-CPSD v2.0.
"""

import numpy as np
from typing import Dict, Any


class ConsumerProfiles:
    """Computes sector-specific load multipliers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_load_multiplier(
        self,
        consumer_type: str,
        time_of_day: np.ndarray,
        ambient_temp: np.ndarray,
        rng: np.random.Generator,
    ) -> np.ndarray:
        n = len(time_of_day)

        if consumer_type == "Residential":
            morning_peak = np.exp(-((time_of_day - 8.0) ** 2) / 3.0) * 1.5
            evening_peak = np.exp(-((time_of_day - 20.0) ** 2) / 4.0) * 2.2
            base_load = 0.5 + morning_peak + evening_peak
            hvac_load = np.abs(ambient_temp - 21.0) * 0.04
            multiplier = base_load + hvac_load + rng.normal(0, 0.1, size=n)

        elif consumer_type == "Commercial":
            business_hours = np.exp(-((time_of_day - 13.0) ** 2) / 18.0) * 3.0
            night_standby = 0.4
            multiplier = night_standby + business_hours + rng.normal(0, 0.15, size=n)

        else:  # Industrial
            shift_variation = 0.2 * np.sin(time_of_day * np.pi / 12.0)
            multiplier = 4.5 + shift_variation + rng.normal(0, 0.2, size=n)

        return np.maximum(multiplier, 0.2).astype(np.float32)
