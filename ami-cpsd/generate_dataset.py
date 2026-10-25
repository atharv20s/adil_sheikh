"""
AMI-CPSD v2.0 Master Dataset Generation Engine.
Implements low-memory streaming generation in 100,000-row chunks to CSV and Parquet.
Exports grid topology (nodes.csv, edges.csv) and simulation timelines (events.csv).
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

import numpy as np
import pandas as pd
import yaml
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulator.scenario import Scenario
from simulator.topology import TopologyGenerator
from simulator.weather import WeatherGenerator
from simulator.physics import PhysicsEngine
from simulator.profiles import ConsumerProfiles
from simulator.meter_state import PersistentMeterEngine
from simulator.kernel import SimulationKernel
from attacks.registry import AttackRegistry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate AMI-CPSD v2.0 Dataset")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/large.yaml",
        help="Path to YAML configuration file",
    )
    return parser.parse_args()


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def generate_chunk(
    config: Dict[str, Any],
    n_samples: int,
    seed: int,
    is_zero_day: bool,
    topology_data: Dict[str, Any],
    kernel: SimulationKernel,
    start_tick: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    num_meters = kernel.num_meters
    ticks_needed = (n_samples + num_meters - 1) // num_meters
    chunk_dfs = []
    for t in range(ticks_needed):
        df_step = kernel.run_step(start_tick + t, rng, is_zero_day=is_zero_day)
        chunk_dfs.append(df_step)
    df_chunk = pd.concat(chunk_dfs, axis=0, ignore_index=True)
    return df_chunk.iloc[:n_samples]


def main():
    args = parse_args()
    start_time = time.time()
    config = load_yaml_config(args.config)
    chunk_size = config.get("chunk_size", 100000)

    base_dir = Path(__file__).resolve().parent
    datasets_dir = base_dir / "datasets"
    metadata_dir = base_dir / "metadata"
    datasets_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Starting {config['dataset_version']} Generation (Config: {args.config} | CHUNK_SIZE={chunk_size:,})...")

    # Export Graph Topology (nodes.csv and edges.csv)
    topo_gen = TopologyGenerator(config)
    topology_data = topo_gen.export_graph_files(datasets_dir, np.random.default_rng(config["seeds"]["train_seed"]))
    logger.info(f"Exported topology nodes.csv & edges.csv to {datasets_dir}")

    attack_registry = AttackRegistry()

    splits = [
        ("train", config["splits"]["train_rows"], config["seeds"]["train_seed"], False),
        ("validation", config["splits"]["val_rows"], config["seeds"]["val_seed"], False),
        ("test", config["splits"]["test_rows"], config["seeds"]["test_seed"], False),
        ("zero_day_test", config["splits"]["zero_day_rows"], config["seeds"]["zero_day_seed"], True),
    ]

    events_list = []

    kernel = SimulationKernel(config, topology_data)
    global_tick = 0

    for split_name, total_rows, seed, is_zero_day in splits:
        csv_path = datasets_dir / f"{split_name}.csv"
        parquet_path = datasets_dir / f"{split_name}.parquet"

        if csv_path.exists():
            csv_path.unlink()
        if parquet_path.exists():
            parquet_path.unlink()

        num_chunks = (total_rows + chunk_size - 1) // chunk_size
        logger.info(f"Streaming {split_name} ({total_rows:,} rows across {num_chunks} chunks)...")

        with tqdm(total=total_rows, desc=f"Streaming {split_name}", unit="rows") as pbar:
            for c_idx in range(num_chunks):
                current_rows = min(chunk_size, total_rows - c_idx * chunk_size)
                chunk_seed = seed + c_idx * 1000

                df_chunk = generate_chunk(
                    config, current_rows, chunk_seed, is_zero_day, topology_data, kernel, start_tick=global_tick
                )
                global_tick += (current_rows + kernel.num_meters - 1) // kernel.num_meters

                # Stream append to CSV
                df_chunk.to_csv(csv_path, mode="a", header=(c_idx == 0), index=False)

                pbar.update(current_rows)

        # Write Parquet file
        df_full_split = pd.read_csv(csv_path)
        df_full_split.to_parquet(parquet_path, index=False)

        file_size_mb = csv_path.stat().st_size / (1024 * 1024)
        logger.info(f"Successfully saved {split_name}.csv ({file_size_mb:.2f} MB) & {split_name}.parquet")

        # Collect event timeline logs
        attack_rows = df_full_split[df_full_split["is_attack"] == 1].head(100)
        for _, row in attack_rows.iterrows():
            events_list.append(
                {
                    "timestamp": row["timestamp"],
                    "meter_id": row["meter_id"],
                    "event": f"Attack Injected ({row['attack_category']})",
                    "stage": row["attack_stage"],
                    "severity": row["attack_severity"],
                }
            )

    # Save events.csv timeline
    df_events = pd.DataFrame(events_list)
    df_events.to_csv(datasets_dir / "events.csv", index=False)
    logger.info(f"Exported simulation timeline to {datasets_dir / 'events.csv'}")

    total_elapsed = time.time() - start_time
    logger.info(f"Dataset generation complete in {total_elapsed:.2f} seconds!")


if __name__ == "__main__":
    main()
