"""
Label Generator Module (AMI-CPSD v1.0).
Generates hierarchical multitask target labels for cyber-physical intrusion detection.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from generator.config import (
    DataConfig,
    ATTACK_MAP,
    STANDARD_ATTACK_DISTRIBUTION,
    ZERO_DAY_ATTACK_DISTRIBUTION,
)


class LabelGenerator:
    """Generates attack target labels and multi-task metadata."""

    def __init__(self, config: DataConfig):
        self.config = config

    def generate_labels(
        self, n_samples: int, is_zero_day_split: bool, rng: np.random.Generator
    ) -> Tuple[np.ndarray, List[str], np.ndarray]:
        """
        Generates attack_type, attack_category, and is_attack columns.

        :param n_samples: Total number of rows to label.
        :param is_zero_day_split: Whether this is the zero_day_test dataset split.
        :param rng: NumPy Random Generator instance.
        :return: Tuple of (attack_type array, attack_category list, is_attack array)
        """
        dist: Dict[int, float] = (
            ZERO_DAY_ATTACK_DISTRIBUTION if is_zero_day_split else STANDARD_ATTACK_DISTRIBUTION
        )

        classes = list(dist.keys())
        probabilities = np.array(list(dist.values()), dtype=float)
        probabilities /= probabilities.sum()

        attack_types = rng.choice(classes, size=n_samples, p=probabilities)
        attack_categories = [ATTACK_MAP[cat_id] for cat_id in attack_types]
        is_attack = (attack_types != 0).astype(int)

        return attack_types, attack_categories, is_attack
