"""
Smart Grid Topology & Graph Generator.
Builds hierarchical grid structure (Substation -> Feeder -> Transformer -> Meter)
and exports adjacency matrix / graph metadata for Graph Neural Network (GNN) models.
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from pathlib import Path
from generator.config import DataConfig


class TopologyGenerator:
    """Generates grid topology hierarchy and GNN spatial graph metadata."""

    def __init__(self, config: DataConfig):
        self.config = config

    def build_topology(self, rng: np.random.Generator) -> Dict[str, Any]:
        """
        Creates hierarchical mapping for smart meters and graph edges.

        :param rng: NumPy Random Generator instance.
        :return: Topology dictionary with meter assignments and graph structure.
        """
        meters = [f"SM-{idx:04d}" for idx in range(1, self.config.num_meters + 1)]
        transformers = [f"XFRM-{idx:02d}" for idx in range(1, self.config.num_transformers + 1)]
        feeders = [f"FDR-{idx:02d}" for idx in range(1, self.config.num_feeders + 1)]
        substations = [f"SUB-{idx:02d}" for idx in range(1, self.config.num_substations + 1)]
        nans = [f"NAN-{idx:02d}" for idx in range(1, self.config.num_nans + 1)]
        dcs = [f"DC-{idx:02d}" for idx in range(1, self.config.num_dcs + 1)]

        meter_to_xfrm = {}
        meter_to_feeder = {}
        meter_to_substation = {}
        meter_to_nan = {}
        meter_to_dc = {}
        coords = {}

        # Hierarchical mapping assignments
        for idx, m_id in enumerate(meters):
            xfrm = transformers[idx % self.config.num_transformers]
            feeder = feeders[(idx // 2) % self.config.num_feeders]
            substation = substations[(idx // 10) % self.config.num_substations]
            nan = nans[idx % self.config.num_nans]
            dc = dcs[(idx // 5) % self.config.num_dcs]

            meter_to_xfrm[m_id] = xfrm
            meter_to_feeder[m_id] = feeder
            meter_to_substation[m_id] = substation
            meter_to_nan[m_id] = nan
            meter_to_dc[m_id] = dc

            # Spatial 2D coordinates (in meters relative to substation center)
            angle = (idx / self.config.num_meters) * 2 * np.pi
            radius = 100.0 + rng.uniform(10.0, 500.0)
            coords[m_id] = {
                "x_meters": round(float(radius * np.cos(angle)), 2),
                "y_meters": round(float(radius * np.sin(angle)), 2),
            }

        # Build Graph Adjacency List (meters sharing same Transformer are connected)
        adjacency_edges = []
        for i, m1 in enumerate(meters):
            for j, m2 in enumerate(meters):
                if i < j and meter_to_xfrm[m1] == meter_to_xfrm[m2]:
                    dx = coords[m1]["x_meters"] - coords[m2]["x_meters"]
                    dy = coords[m1]["y_meters"] - coords[m2]["y_meters"]
                    distance = float(np.sqrt(dx**2 + dy**2))
                    adjacency_edges.append(
                        {
                            "source": m1,
                            "target": m2,
                            "transformer": meter_to_xfrm[m1],
                            "distance_m": round(distance, 2),
                            "impedance_ohm": round(distance * 0.0005, 4),
                            "comm_link": "802.15.4g_Mesh",
                        }
                    )

        topology_data = {
            "version": "AMI-CPSD Topology v1.0",
            "num_meters": len(meters),
            "num_transformers": len(transformers),
            "num_feeders": len(feeders),
            "num_substations": len(substations),
            "meter_assignments": {
                m_id: {
                    "substation_id": meter_to_substation[m_id],
                    "feeder_id": meter_to_feeder[m_id],
                    "transformer_id": meter_to_xfrm[m_id],
                    "nan_id": meter_to_nan[m_id],
                    "dc_id": meter_to_dc[m_id],
                    "coordinates": coords[m_id],
                }
                for m_id in meters
            },
            "graph_edges": adjacency_edges,
        }

        return topology_data

    def export_graph_json(self, output_path: Path, rng: np.random.Generator):
        """Exports graph topology structure to metadata JSON file for GNN model consumption."""
        topology_data = self.build_topology(rng)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(topology_data, f, indent=4)
        return topology_data
