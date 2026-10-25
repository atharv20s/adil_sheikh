"""
Unit Tests for AMI-CPSD v2.0 Physics Engine.
"""

import sys
import os
import numpy as np
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.physics import PhysicsEngine


def test_power_physics_validation():
    config = {"simulation": {"physics_tolerance_kw": 0.05}}
    physics = PhysicsEngine(config)

    voltage = np.array([230.0, 220.0], dtype=np.float32)
    current = np.array([10.0, 5.0], dtype=np.float32)
    power_factor = np.array([0.95, 0.90], dtype=np.float32)
    active_power = np.array([0.0, 0.0], dtype=np.float32)  # Wrong initial values
    is_attack = np.array([0, 0], dtype=np.int32)

    p_act, q_act, s_act = physics.validate_and_correct_power_physics(
        voltage, current, power_factor, active_power, is_attack
    )

    expected_p0 = (230.0 * 10.0 * 0.95) / 1000.0
    assert np.isclose(p_act[0], expected_p0, atol=1e-3)
    assert p_act[0] > 0.0
    assert q_act[0] >= 0.0
    assert s_act[0] >= p_act[0]


def test_ou_process_bounds():
    config = {}
    physics = PhysicsEngine(config)
    rng = np.random.default_rng(42)

    ou_series = physics.generate_ou_process(
        n_samples=1000, mean=229.0, theta=0.8, sigma=0.6, dt=0.25, initial_val=229.0, rng=rng
    )

    assert len(ou_series) == 1000
    assert np.all(np.isfinite(ou_series))
    assert 200.0 < np.mean(ou_series) < 250.0
