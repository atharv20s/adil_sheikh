"""
Smart Grid Topology & Graph Exporter for AMI-CPSD v2.0.
Exports hierarchical structure to nodes.csv and edges.csv for GNN frameworks (PyG, DGL, NetworkX).
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, Any
from pathlib import Path


class TopologyGenerator:
    """Generates grid topology hierarchy and exports GNN graph node/edge lists."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        topo_cfg = config.get("topology", {})
        self.num_substations = topo_cfg.get("num_substations", 2)
        self.num_feeders = topo_cfg.get("num_feeders", 6)
        self.num_transformers = topo_cfg.get("num_transformers", 20)
        self.num_meters = topo_cfg.get("num_meters", 100)
        self.num_nans = topo_cfg.get("num_nans", 10)
        self.num_dcs = topo_cfg.get("num_dcs", 4)

    def build_topology(self, rng: np.random.Generator) -> Dict[str, Any]:
        meters = [f"SM-{idx:04d}" for idx in range(1, self.num_meters + 1)]
        transformers = [f"XFRM-{idx:02d}" for idx in range(1, self.num_transformers + 1)]
        feeders = [f"FDR-{idx:02d}" for idx in range(1, self.num_feeders + 1)]
        substations = [f"SUB-{idx:02d}" for idx in range(1, self.num_substations + 1)]
        nans = [f"NAN-{idx:02d}" for idx in range(1, self.num_nans + 1)]
        dcs = [f"DC-{idx:02d}" for idx in range(1, self.num_dcs + 1)]

        meter_map = {}
        coords = {}

        for idx, m_id in enumerate(meters):
            xfrm = transformers[idx % self.num_transformers]
            feeder = feeders[(idx // 2) % self.num_feeders]
            substation = substations[(idx // 10) % self.num_substations]
            nan = nans[idx % self.num_nans]
            dc = dcs[(idx // 5) % self.num_dcs]

            angle = (idx / self.num_meters) * 2 * np.pi
            radius = 100.0 + rng.uniform(10.0, 500.0)
            x_m = round(float(radius * np.cos(angle)), 2)
            y_m = round(float(radius * np.sin(angle)), 2)

            meter_map[m_id] = {
                "substation_id": substation,
                "feeder_id": feeder,
                "transformer_id": xfrm,
                "nan_id": nan,
                "dc_id": dc,
                "coordinates": {"x_meters": x_m, "y_meters": y_m},
            }
            coords[m_id] = (x_m, y_m)

        edges = []
        for i, m1 in enumerate(meters):
            for j, m2 in enumerate(meters):
                if i < j and meter_map[m1]["transformer_id"] == meter_map[m2]["transformer_id"]:
                    dx = coords[m1][0] - coords[m2][0]
                    dy = coords[m1][1] - coords[m2][1]
                    dist = float(np.sqrt(dx**2 + dy**2))
                    edges.append(
                        {
                            "source_node": m1,
                            "target_node": m2,
                            "transformer_id": meter_map[m1]["transformer_id"],
                            "distance_m": round(dist, 2),
                            "impedance_ohm": round(dist * 0.0005, 4),
                            "link_type": "802.15.4g_Mesh",
                        }
                    )

        return {"meter_assignments": meter_map, "edges": edges}

    def export_graph_files(self, output_dir: Path, rng: np.random.Generator):
        """Exports nodes.csv and edges.csv for GNN frameworks."""
        output_dir.mkdir(parents=True, exist_ok=True)
        topo = self.build_topology(rng)

        # 1. Export nodes.csv
        node_rows = []
        for m_id, data in topo["meter_assignments"].items():
            node_rows.append(
                {
                    "node_id": m_id,
                    "node_type": "smart_meter",
                    "substation_id": data["substation_id"],
                    "feeder_id": data["feeder_id"],
                    "transformer_id": data["transformer_id"],
                    "nan_id": data["nan_id"],
                    "dc_id": data["dc_id"],
                    "x_meters": data["coordinates"]["x_meters"],
                    "y_meters": data["coordinates"]["y_meters"],
                }
            )
        df_nodes = pd.DataFrame(node_rows)
        df_nodes.to_csv(output_dir / "nodes.csv", index=False)

        # 2. Export edges.csv
        df_edges = pd.DataFrame(topo["edges"])
        df_edges.to_csv(output_dir / "edges.csv", index=False)

        return topo
