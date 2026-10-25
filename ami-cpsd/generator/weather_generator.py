"""
Weather & Environmental Data Generator.
Simulates meteorological factors and temporal cycles that drive smart grid thermal loading.
"""

import numpy as np
import pandas as pd
from generator.config import DataConfig


class WeatherGenerator:
    """Generates environmental weather features coupled with temporal profiles."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate(
        self, n_samples: int, time_offsets_hours: np.ndarray, rng: np.random.Generator
    ) -> pd.DataFrame:
        """
        Generates realistic weather telemetry based on time of day and season.

        :param n_samples: Number of observations.
        :param time_offsets_hours: Hour offsets for diurnal solar/temperature modeling.
        :param rng: NumPy Random Generator instance.
        :return: DataFrame containing environmental features.
        """
        time_of_day = time_offsets_hours % 24.0
        day_of_week = ((time_offsets_hours // 24.0) % 7.0).astype(int)
        is_holiday = rng.choice([0, 1], size=n_samples, p=[0.95, 0.05])

        # Diurnal Ambient Temperature (°C): Min around 5 AM, Max around 3 PM
        solar_phase = np.sin((time_of_day - 9.0) * np.pi / 12.0)
        base_temp = 22.0 + 8.0 * solar_phase
        temp_noise = rng.normal(loc=0.0, scale=1.5, size=n_samples)
        ambient_temperature = base_temp + temp_noise
        ambient_temperature = np.clip(ambient_temperature, -5.0, 42.0)

        # Humidity (% RH): Inverse relationship with temperature
        humidity = 70.0 - 1.2 * (ambient_temperature - 20.0) + rng.normal(0, 5.0, size=n_samples)
        humidity = np.clip(humidity, 15.0, 98.0)

        # Solar Irradiance (W/m²): 0 at night (6 PM to 6 AM), bell curve during daylight
        daylight_mask = (time_of_day >= 6.0) & (time_of_day <= 18.0)
        solar_irradiance = np.zeros(n_samples)
        solar_irradiance[daylight_mask] = 950.0 * np.sin(
            (time_of_day[daylight_mask] - 6.0) * np.pi / 12.0
        )
        solar_irradiance += rng.normal(0.0, 20.0, size=n_samples)
        solar_irradiance = np.maximum(solar_irradiance, 0.0)

        # Wind Speed (m/s): Weibull / Rayleigh distribution
        wind_speed = rng.weibull(a=2.0, size=n_samples) * 4.5
        wind_speed = np.clip(wind_speed, 0.2, 22.0)

        df = pd.DataFrame(
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

        return df
