"""
Closed-Loop Consensus & Blockchain Feedback Engine for AMI-CPSD v3.0.
Models cyber-physical feedback loops between consensus voting, PBFT retries, 
block latency, queue length, and network packet delay.
"""

import numpy as np
from typing import Dict, Any, Tuple


class ClosedLoopConsensusEngine:
    """Calculates network and blockchain feedback interactions."""
    def __init__(self, num_nodes: int = 100):
        self.num_nodes = num_nodes

    def step(
        self,
        byzantine_votes: np.ndarray,
        failed_consensus: np.ndarray,
        base_packet_delay: np.ndarray,
        rng: np.random.Generator
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Feedback Loop:
        High Byzantine votes / failed consensus -> PBFT retries ->
        Increases block latency -> Backlogs network queues -> Increases packet delay & loss.
        """
        # Consensus Latency = Base (120ms) + 150ms * byzantine_votes + 300ms * failed_consensus
        consensus_latency = 120.0 + 150.0 * byzantine_votes + 300.0 * failed_consensus + rng.normal(0, 10.0, size=self.num_nodes)
        consensus_latency = np.clip(consensus_latency, 80.0, 4500.0).astype(np.float32)

        # Queue Length backlogs under high consensus latency
        queue_length = np.clip(15.0 + (consensus_latency - 120.0) * 0.4 + rng.poisson(2.0, size=self.num_nodes), 1.0, 1000.0).astype(np.float32)

        # Network Packet Delay increases dynamically with Queue Backlog
        effective_packet_delay = base_packet_delay + (queue_length * 0.8)

        # Packet Loss Rate increases under heavy queue congestion
        packet_loss = np.clip((queue_length / 200.0) * 2.5 + rng.exponential(0.2, size=self.num_nodes), 0.0, 25.0).astype(np.float32)

        return consensus_latency, queue_length, effective_packet_delay, packet_loss
