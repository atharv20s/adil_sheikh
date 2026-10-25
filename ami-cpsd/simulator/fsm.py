"""
Meter Finite State Machine (FSM) for AMI-CPSD v3.0.
Models multi-stage cyber-physical attack transitions:
Normal -> Recon -> Exploit -> Escalation -> Persistence -> Impact -> Recovery -> Normal.
"""

import numpy as np
from enum import Enum
from typing import Dict, List


class AttackStageFSM(Enum):
    NORMAL = 0
    RECON = 1
    EXPLOIT = 2
    ESCALATION = 3
    PERSISTENCE = 4
    IMPACT = 5
    RECOVERY = 6


class MeterFSM:
    """Manages attack state machine transitions per smart meter."""
    def __init__(self, meter_id: str):
        self.meter_id = meter_id
        self.state = AttackStageFSM.NORMAL
        self.ticks_in_state = 0
        self.target_attack_type = 0

    def trigger_attack(self, attack_type: int):
        """Initiates an attack lifecycle."""
        if self.state == AttackStageFSM.NORMAL:
            self.target_attack_type = attack_type
            self.state = AttackStageFSM.RECON
            self.ticks_in_state = 0

    def step(self, rng: np.random.Generator) -> AttackStageFSM:
        """Transitions FSM forward one simulation step based on transition probabilities."""
        self.ticks_in_state += 1

        if self.state == AttackStageFSM.NORMAL:
            pass # Stays normal until triggered

        elif self.state == AttackStageFSM.RECON:
            if self.ticks_in_state > 2 and rng.random() < 0.6:
                self.state = AttackStageFSM.EXPLOIT
                self.ticks_in_state = 0

        elif self.state == AttackStageFSM.EXPLOIT:
            if self.ticks_in_state > 3 and rng.random() < 0.7:
                self.state = AttackStageFSM.ESCALATION
                self.ticks_in_state = 0

        elif self.state == AttackStageFSM.ESCALATION:
            if self.ticks_in_state > 2 and rng.random() < 0.8:
                self.state = AttackStageFSM.IMPACT
                self.ticks_in_state = 0

        elif self.state == AttackStageFSM.IMPACT:
            if self.ticks_in_state > 8 and rng.random() < 0.4:
                self.state = AttackStageFSM.RECOVERY
                self.ticks_in_state = 0

        elif self.state == AttackStageFSM.RECOVERY:
            if self.ticks_in_state > 3:
                self.state = AttackStageFSM.NORMAL
                self.ticks_in_state = 0
                self.target_attack_type = 0

        return self.state

    def get_stage_name(self) -> str:
        return self.state.name.title()
