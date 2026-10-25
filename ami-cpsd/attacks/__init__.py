"""
Pluggable Attack Package for AMI-CPSD v2.0.
"""

from .base import Attack
from .registry import AttackRegistry

__all__ = ["Attack", "AttackRegistry"]
