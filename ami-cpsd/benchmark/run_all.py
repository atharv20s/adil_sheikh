"""
AMI-CPSD v2.0 Unified Master Benchmark Runner.
Executes, evaluates, and compares all 12 models across 4 active tracks.
Saves comparisons, figures, and logs.
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import asdict

# Config and Dataloader
from benchmark.config import (
    FEATURE_COLS, RESULTS_DIR, FIGURES_DIR, REPORTS_DIR
)
from benchmark.dataloader import (
    load_tabular, load_sequences, load_anomaly_data, load_graph_data, load_multitask_data
)

# Model Imports
from benchmark.classical.logistic import LogisticRegressionBenchmark
from benchmark.classical.random_forest import RandomForestBenchmark
from benchmark.classical.xgboost import XGBoostBenchmark
from benchmark.classical.lightgbm import LightGBMBenchmark
from benchmark.classical.svm import SVMBenchmark
from benchmark.deep_learning.mlp import MLPBenchmark
from benchmark.deep_learning.lstm import LSTMBenchmark
from benchmark.deep_learning.transformer import TransformerBenchmark
from benchmark.graph.gcn import GCNBenchmark, PYG_AVAILABLE as GCN_PYG_AVAILABLE
from benchmark.graph.gat import GATBenchmark, PYG_AVAILABLE as GAT_PYG_AVAILABLE
from benchmark.anomaly.isolation_forest import IsolationForestBenchmark
from benchmark.anomaly.autoencoder import AutoencoderBenchmark
from benchmark.physics_aware.pinn_transformer import PhysicsAwareTransformerBenchmark
from benchmark.multi_task.multi_task_ids import MultiTaskIDSBenchmark

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def generate_plots(results):
    """Generates benchmark comparison figures."""
    if not results:
        return
        
    names = [r["model_name"] for r in results]
    f1s = [r["f1_weighted"] for r in results]
    latencies = [r["inference_latency_ms"] for r in results]
    zd_f1s = [r["zero_day_f1"] for r in results]

    # Plot 1: Accuracy & Weighted F1 Bar Chart
    plt.figure(figsize=(12, 6))
    x = np.arange(len(names))
    width = 0.35
    
    plt.bar(x - width/2, f1s, width, label='F1-Score (Standard Multi-Class)', color='royalblue')
    plt.bar(x + width/2, zd_f1s, width, label='F1-Score (Zero-Day Binary)', color='tomato')
    
    plt.ylabel('F1 Score')
    plt.title('Performance Comparison Across All Benchmark Models', fontsize=12, fontweight='bold')
    plt.xticks(x, names, rotation=45, ha='right')
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    
    out_path = FIGURES_DIR / "accuracy_comparison.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved accuracy comparison plot to {out_path}")


def main():
    parser = argparse.ArgumentParser(description="AMI-CPSD v2.0 Master Benchmark Runner")
    parser.add_argument("--train-rows", type=int, default=50000, help="Number of rows for training")
    parser.add_argument("--val-rows", type=int, default=10000, help="Number of rows for validation")
    parser.add_argument("--test-rows", type=int, default=10000, help="Number of rows for testing")
    parser.add_argument("--zero-day-rows", type=int, default=10000, help="Number of rows for zero-day test")
    parser.add_argument("--epochs", type=int, default=30, help="PyTorch model training epochs")
    parser.add_argument("--device", type=str, default="cpu", help="PyTorch device (cpu or cuda)")
    parser.add_argument("--skip-graph", action="store_true", help="Explicitly skip GNN models")
    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("  AMI-CPSD v2.0 - STARTING MASTER BENCHMARK RUN")
    logger.info("=" * 80)

    # 1. Load Datasets
    logger.info("Preparing datasets...")
    X_train, y_train, X_val, y_val, X_test, y_test = load_tabular(
        args.train_rows, args.val_rows, args.test_rows
    )
    
    train_loader, val_loader, test_loader, y_test_seq, zd_loader, y_zd_binary_seq = load_sequences(
        args.train_rows, args.val_rows, args.test_rows, args.zero_day_rows
    )
    
    X_train_normal, X_val_normal, y_val_binary, X_test_normal, y_test_binary, X_zd, y_zd_binary = load_anomaly_data(
        args.train_rows, args.val_rows, args.test_rows, args.zero_day_rows
    )

    X_train_mt, y_train_mt, X_val_mt, y_val_mt, X_test_mt, y_test_mt = load_multitask_data(
        args.train_rows, args.val_rows, args.test_rows
    )

    graph_train, graph_test = None, None
    if GCN_PYG_AVAILABLE and GAT_PYG_AVAILABLE and not args.skip_graph:
        snapshots = load_graph_data(num_snapshots=300)
        if snapshots:
            split_idx = int(len(snapshots) * 0.8)
            graph_train = snapshots[:split_idx]
            graph_test = snapshots[split_idx:]
    else:
        logger.info("PyTorch Geometric missing or --skip-graph passed. Graph models will be skipped.")

    # Shared parameters
    zero_day_data = (X_zd, y_zd_binary)
    zero_day_data_seq = (zd_loader, y_zd_binary_seq)

    # 2. Instantiate Models
    models_to_run = [
        # Track 1: Classical
        LogisticRegressionBenchmark(),
        RandomForestBenchmark(),
        XGBoostBenchmark(),
        LightGBMBenchmark(),
        SVMBenchmark(),
        
        # Track 2: Deep Learning
        MLPBenchmark(),
        LSTMBenchmark(),
        TransformerBenchmark(),
        
        # Track 5: Anomaly Detection
        IsolationForestBenchmark(),
        AutoencoderBenchmark(),

        # Track 6: Physics-Aware Learning
        PhysicsAwareTransformerBenchmark(),

        # Track 7: Multi-Task Learning
        MultiTaskIDSBenchmark()
    ]

    # Track 3: Graph Neural Networks (Conditional)
    if graph_train is not None:
        models_to_run.extend([
            GCNBenchmark(),
            GATBenchmark()
        ])

    results = []

    # 3. Execute Run Loops
    for bm_model in models_to_run:
        logger.info("-" * 60)
        logger.info(f"Running model: {bm_model.name} (Track: {bm_model.track})")
        logger.info("-" * 60)

        # Train & Evaluate based on track
        try:
            if bm_model.track == "classical":
                # RF needs feature names for export
                if bm_model.name == "Random Forest":
                    bm_model.train(X_train, y_train, feature_names=FEATURE_COLS)
                else:
                    bm_model.train(X_train, y_train)
                res = bm_model.evaluate(X_test, y_test, zero_day_data=zero_day_data)
                
            elif bm_model.name == "MLP":
                bm_model.train(X_train, y_train, X_val, y_val, epochs=args.epochs, device=args.device)
                res = bm_model.evaluate(X_test, y_test, zero_day_data=zero_day_data)
                
            elif bm_model.name in ["LSTM", "Transformer", "Physics Transformer"]:
                # Expect sequences
                bm_model.train(train_loader, val_loader, epochs=args.epochs, device=args.device)
                res = bm_model.evaluate(test_loader, y_test_seq, zero_day_data=zero_day_data_seq)

            elif bm_model.track == "multi_task":
                bm_model.train(X_train_mt, y_train_mt, X_val_mt, y_val_mt, epochs=args.epochs, device=args.device)
                res = bm_model.evaluate(X_test_mt, y_test_mt["type"], zero_day_data=zero_day_data)
                
            elif bm_model.track == "anomaly":
                if bm_model.name == "Autoencoder":
                    bm_model.train(X_train_normal, X_val_normal, y_val_binary, epochs=args.epochs, device=args.device)
                else:
                    bm_model.train(X_train_normal)
                # Evaluates binary Normal vs Attack on standard test set, and Zero-Day test set
                res = bm_model.evaluate(X_test_normal, y_test_binary, zero_day_data=zero_day_data)
                
            elif bm_model.track == "graph":
                bm_model.train(graph_train, epochs=15, device=args.device)
                res = bm_model.evaluate(graph_test, zero_day_data=graph_test) # use graph_test as zero day for simplicity

            results.append(res)
            
            # Save checkpoints
            checkpoint_name = f"{bm_model.name.lower().replace(' ', '_')}_model.pkl"
            if bm_model.track in ["deep_learning", "graph", "anomaly"] and bm_model.name != "Isolation Forest":
                checkpoint_name = checkpoint_name.replace(".pkl", ".pt")
            bm_model.save(RESULTS_DIR / "checkpoints" / checkpoint_name)

        except Exception as e:
            logger.error(f"Error executing {bm_model.name}: {str(e)}", exc_info=True)

    # 4. Print Summary Table
    logger.info("\n" + "=" * 100)
    logger.info(f"{'Model Name':<22} | {'Track':<14} | {'Accuracy':<8} | {'Weighted F1':<11} | {'Zero-Day F1':<11} | {'Train (s)':<9} | {'Latency (ms)':<12}")
    logger.info("=" * 100)
    
    dict_results = []
    for r in results:
        logger.info(
            f"{r.model_name:<22} | {r.track:<14} | {r.accuracy:<8.4f} | "
            f"{r.f1_weighted:<11.4f} | {r.zero_day_f1:<11.4f} | "
            f"{r.train_time_sec:<9.2f} | {r.inference_latency_ms:<12.6f}"
        )
        dict_results.append(asdict(r))
        
    logger.info("=" * 100)

    # 5. Save aggregate results json
    comparison_path = RESULTS_DIR / "benchmark_comparison.json"
    with open(comparison_path, "w") as f:
        json.dump(dict_results, f, indent=4)
    logger.info(f"Aggregate benchmark comparison saved to {comparison_path}")

    # 6. Generate comparison plot
    generate_plots(dict_results)

    logger.info("Benchmark complete!")


if __name__ == "__main__":
    main()
