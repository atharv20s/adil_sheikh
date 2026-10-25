"""
Attack Registry Factory for AMI-CPSD v2.0.
"""

from typing import Dict, Type
from attacks.base import Attack
from attacks.dos import DoSAttack, DDoSAttack
from attacks.network import ReplayAttack, MITMAttack
from attacks.physical import FDIAttack, DataTamperingAttack, InsiderAttack
from attacks.consensus import SybilAttack, ByzantineAttack, KeyTheftAttack
from attacks.device import FirmwareAttack, MalwareAttack


class AttackRegistry:
    """Registry mapping integer attack class IDs and names to attack instances."""

    def __init__(self):
        self._registry: Dict[int, Attack] = {}
        self._register_default_attacks()

    def register(self, attack: Attack):
        """Registers a new pluggable attack instance."""
        self._registry[attack.attack_id] = attack

    def get_attack(self, attack_id: int) -> Attack:
        """Retrieves attack instance by integer class ID."""
        if attack_id not in self._registry:
            raise KeyError(f"No attack registered for attack_id={attack_id}")
        return self._registry[attack_id]

    def _register_default_attacks(self):
        self.register(DoSAttack())
        self.register(DDoSAttack())
        self.register(ReplayAttack())
        self.register(MITMAttack())
        self.register(FDIAttack())
        self.register(SybilAttack())
        self.register(ByzantineAttack())
        self.register(FirmwareAttack())
        self.register(KeyTheftAttack())
        self.register(DataTamperingAttack())
        self.register(InsiderAttack())
        self.register(MalwareAttack())
