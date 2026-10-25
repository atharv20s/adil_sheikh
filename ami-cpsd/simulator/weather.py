"""
Weather Data Generator for AMI-CPSD v2.0.
Simulates environmental conditions driving electrical HVAC loads.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class WeatherGenerator:
    """Generates weather and environmental parameters."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate(
        self, n_samples: int, time_offsets_hours: np.ndarray, rng: np.random.Generator
    ) -> pd.DataFrame:
        """
        Generates weather telemetry.
        """
        time_of_day = (time_offsets_hours % 24.0).astype(np.float32)
        day_of_week = ((time_offsets_hours // 24.0) % 7.0).astype(np.int32)
        is_holiday = rng.choice([0, 1], size=n_samples, p=[0.95, 0.05]).astype(np.int32)

        solar_phase = np.sin((time_of_day - 9.0) * np.pi / 12.0)
        base_temp = 22.0 + 8.0 * solar_phase
        temp_noise = rng.normal(loc=0.0, scale=1.5, size=n_samples)
        ambient_temperature = np.clip(base_temp + temp_noise, -5.0, 42.0).astype(np.float32)

        humidity = np.clip(70.0 - 1.2 * (ambient_temperature - 20.0) + rng.normal(0, 5.0, size=n_samples), 15.0, 98.0).astype(np.float32)

        daylight_mask = (time_of_day >= 6.0) & (time_of_day <= 18.0)
        solar_irradiance = np.zeros(n_samples, dtype=np.float32)
        solar_irradiance[daylight_mask] = 950.0 * np.sin((time_of_day[daylight_mask] - 6.0) * np.pi / 12.0)
        solar_irradiance = np.maximum(solar_irradiance + rng.normal(0.0, 20.0, size=n_samples), 0.0).astype(np.float32)

        wind_speed = np.clip(rng.weibull(a=2.0, size=n_samples) * 4.5, 0.2, 22.0).astype(np.float32)

        return pd.DataFrame(
            {
                "ambient_temperature": np.round(ambient_temperature, 2),
                "humidity": np.round(humidity, 2),
                "solar_irradiance": np.round(solar_irradiance, 2),
                "wind_speed": np.round(wind_speed, 2),
                "time_of_day": np.round(time_of_day, 2),
                "day_of_week": day_of_week,
                "is_holiday": is_holiday,
            }
        )
