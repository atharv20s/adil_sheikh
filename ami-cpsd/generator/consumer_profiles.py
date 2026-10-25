"""
Consumer Load Profiles Module.
Simulates realistic electricity consumption behavior for Residential, Commercial, and Industrial grid sectors.
"""

import numpy as np
import pandas as pd
from typing import Tuple
from generator.config import DataConfig


class ConsumerProfiles:
    """Generates sector-specific load multipliers based on time and weather."""

    def __init__(self, config: DataConfig):
        self.config = config

    def get_load_multiplier(
        self,
        consumer_type: str,
        time_of_day: np.ndarray,
        ambient_temp: np.ndarray,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """
        Computes active current/power scale factor.

        :param consumer_type: "Residential", "Commercial", or "Industrial"
        :param time_of_day: Array of hour values (0.0 to 23.99).
        :param ambient_temp: Array of ambient temperatures in °C.
        :param rng: NumPy Random Generator instance.
        :return: Array of load multipliers.
        """
        n = len(time_of_day)

        if consumer_type == "Residential":
            # Morning peak (7-9 AM) and Evening peak (6-10 PM)
            morning_peak = np.exp(-((time_of_day - 8.0) ** 2) / 3.0) * 1.5
            evening_peak = np.exp(-((time_of_day - 20.0) ** 2) / 4.0) * 2.2
            base_load = 0.5 + morning_peak + evening_peak
            # HVAC cooling/heating factor
            hvac_load = np.abs(ambient_temp - 21.0) * 0.04
            multiplier = base_load + hvac_load + rng.normal(0, 0.1, size=n)

        elif consumer_type == "Commercial":
            # Business hours load profile (8 AM to 6 PM)
            business_hours = np.exp(-((time_of_day - 13.0) ** 2) / 18.0) * 3.0
            night_standby = 0.4
            multiplier = night_standby + business_hours + rng.normal(0, 0.15, size=n)

        else:  # Industrial
            # Continuous high load profile 24/7 with minor shift variations
            shift_variation = 0.2 * np.sin(time_of_day * np.pi / 12.0)
            multiplier = 4.5 + shift_variation + rng.normal(0, 0.2, size=n)

        return np.maximum(multiplier, 0.2)
