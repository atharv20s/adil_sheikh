"""
Persistent Per-Meter State Manager for AMI-CPSD Digital Twin.
Maintains continuous Ornstein-Uhlenbeck (OU) states, consumer profiles, 
and electrical impedance parameters for each individual smart meter.
"""

import numpy as np
from typing import Dict, List, Any


class MeterState:
    """Represents the continuous temporal state of a single smart meter."""
    def __init__(self, meter_id: str, node_idx: int, profile: str, feeder_distance_m: float):
        self.meter_id = meter_id
        self.node_idx = node_idx
        self.profile = profile # Fixed forever: Residential, Commercial, Industrial, EV_Station
        self.feeder_distance_m = feeder_distance_m
        
        # Base physical parameters by profile
        if profile == "Industrial":
            self.base_v = 240.0
            self.base_i = 45.0
            self.base_pf = 0.95
        elif profile == "Commercial":
            self.base_v = 230.0
            self.base_i = 25.0
            self.base_pf = 0.92
        elif profile == "EV_Station":
            self.base_v = 230.0
            self.base_i = 35.0
            self.base_pf = 0.98
        else: # Residential
            self.base_v = 230.0
            self.base_i = 10.0
            self.base_pf = 0.90

        # Continuous state variables (OU Process)
        self.voltage = self.base_v
        self.current = self.base_i
        self.power_factor = self.base_pf
        self.temperature = 25.0
        self.cpu_usage = 15.0
        self.memory_usage = 30.0

    def update_ou(self, dt: float = 1.0, theta: float = 0.15, sigma_v: float = 0.5, sigma_i: float = 1.0):
        """Updates continuous state using Ornstein-Uhlenbeck mean-reverting process."""
        # Voltage OU process
        dv = theta * (self.base_v - self.voltage) * dt + sigma_v * np.random.normal() * np.sqrt(dt)
        self.voltage = np.clip(self.voltage + dv, 200.0, 260.0)
        
        # Current OU process
        di = theta * (self.base_i - self.current) * dt + sigma_i * np.random.normal() * np.sqrt(dt)
        self.current = np.clip(self.current + di, 0.5, 120.0)
        
        # Power factor slight variation
        dpf = theta * (self.base_pf - self.power_factor) * dt + 0.005 * np.random.normal() * np.sqrt(dt)
        self.power_factor = np.clip(self.power_factor + dpf, 0.70, 0.99)
        
        # CPU variation
        dcpu = theta * (15.0 - self.cpu_usage) * dt + 1.0 * np.random.normal() * np.sqrt(dt)
        self.cpu_usage = np.clip(self.cpu_usage + dcpu, 5.0, 40.0)


class PersistentMeterEngine:
    """Global manager for all meters in the simulation grid."""
    def __init__(self, num_meters: int = 100):
        self.num_meters = num_meters
        profiles_pool = ["Residential"] * 60 + ["Commercial"] * 25 + ["Industrial"] * 10 + ["EV_Station"] * 5
        np.random.seed(42)
        np.random.shuffle(profiles_pool)

        self.meters: Dict[str, MeterState] = {}
        self.meter_ids: List[str] = [f"SM-{i+1:04d}" for i in range(num_meters)]

        for idx, mid in enumerate(self.meter_ids):
            dist = (idx + 1) * 25.0 # Feeder distance along line (meters)
            prof = profiles_pool[idx]
            self.meters[mid] = MeterState(mid, idx, prof, dist)

    def get_state(self, meter_id: str) -> MeterState:
        return self.meters[meter_id]

    def step_all(self, dt: float = 1.0):
        """Steps all meters forward in time by dt."""
        for m in self.meters.values():
            m.update_ou(dt=dt)
