"""
Unit Tests for AMI-CPSD v2.0 Pluggable Attack Engine.
"""

import sys
import os
import numpy as np
import pandas as pd
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from attacks.registry import AttackRegistry


def test_attack_registry_and_perturbations():
    registry = AttackRegistry()
    dos_attack = registry.get_attack(1)

    assert dos_attack.name == "DoS"
    assert dos_attack.domain == "Network"
    assert "packet_rate" in dos_attack.affected_features

    df = pd.DataFrame(
        {
            "packet_rate": [12.0, 12.0],
            "cpu_usage": [25.0, 25.0],
            "ram_usage": [35.0, 35.0],
            "packet_delay": [10.0, 10.0],
            "queue_length": [15.0, 15.0],
        }
    )

    rng = np.random.default_rng(42)
    indices = np.array([0])
    df_perturbed = dos_attack.apply(df, indices, severity="High", stage="Impact", rng=rng)

    assert df_perturbed.at[0, "packet_rate"] > 100.0
    assert df_perturbed.at[1, "packet_rate"] == 12.0
