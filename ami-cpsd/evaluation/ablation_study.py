"""
Ablation Study Module for AMI-CPSD v3.0.
Evaluates model performance across 6 simulator ablation configurations:
1. Full Simulator (Baseline)
2. Without Weather (Excludes ambient_temperature, humidity, solar_irradiance, wind_speed)
3. Without Physics (Excludes active_power, reactive_power, apparent_power, power_factor)
4. Without Consensus (Excludes consensus_latency, validator_votes, failed_consensus, queue_length)
5. Without IDS Anomaly Scores (Excludes anomaly_score, drift_score, isolation_forest_score, autoencoder_score)
6. Without Device Telemetry (Excludes cpu_usage, ram_usage, temperature, flash_usage)
"""

import json
import logging
import sys
import numpy as np
import pandas as pd
from pathlib import Path

from benchmark.config import FEATURE_COLS, RESULTS_DIR
from benchmark.dataloader import load_tabular, load_anomaly_data
from benchmark.classical.random_forest import RandomForestBenchmark
from benchmark.classical.xgboost import XGBoostBenchmark
from benchmark.deep_learning.mlp import MLPBenchmark
from benchmark.physics_aware.pinn_transformer import PhysicsAwareTransformerBenchmark

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


ABLATION_FEATURE_GROUPS = {
    "Full Simulator": FEATURE_COLS,
    "Without Weather": [c for c in FEATURE_COLS if c not in ["ambient_temperature", "humidity", "solar_irradiance", "wind_speed", "time_of_day"]],
    "Without Physics": [c for c in FEATURE_COLS if c not in ["active_power", "reactive_power", "apparent_power", "power_factor", "voltage", "current"]],
    "Without Consensus": [c for c in FEATURE_COLS if c not in ["consensus_latency", "transaction_delay", "validator_votes", "failed_consensus", "queue_length", "byzantine_votes"]],
    "Without IDS Anomaly": [c for c in FEATURE_COLS if c not in ["anomaly_score", "drift_score", "isolation_forest_score", "autoencoder_score", "svm_score", "entropy", "packet_diversity"]],
    "Without Device Telemetry": [c for c in FEATURE_COLS if c not in ["cpu_usage", "ram_usage", "flash_usage", "temperature", "battery", "firmware_hash_valid", "reboot_count"]],
}


def run_ablation_study(train_rows=10000, val_rows=5000, test_rows=5000):
    logger.info("=" * 80)
    logger.info("  STARTING AMI-CPSD v3.0 ABLATION STUDY")
    logger.info("=" * 80)

    X_train, y_train, X_val, y_val, X_test, y_test = load_tabular(train_rows, val_rows, test_rows)
    X_train_norm, X_val_norm, y_val_bin, X_test_norm, y_test_bin, X_zd, y_zd_bin = load_anomaly_data(train_rows, val_rows, test_rows, test_rows)

    ablation_results = []

    for name, cols in ABLATION_FEATURE_GROUPS.items():
        logger.info(f"\n--- Running Ablation Configuration: {name} ({len(cols)} features) ---")
        indices = [FEATURE_COLS.index(c) for c in cols]
        
        X_tr_sub = X_train[:, indices]
        X_te_sub = X_test[:, indices]
        X_zd_sub = X_zd[:, indices]
        
        # Benchmark with XGBoost as reference model
        model = XGBoostBenchmark()
        model.train(X_tr_sub, y_train)
        res = model.evaluate(X_te_sub, y_test, zero_day_data=(X_zd_sub, y_zd_bin))

        row = {
            "config": name,
            "feature_count": len(cols),
            "accuracy": res.accuracy,
            "f1_weighted": res.f1_weighted,
            "zero_day_f1": res.zero_day_f1,
            "latency_ms": res.inference_latency_ms
        }
        ablation_results.append(row)
        logger.info(f"[{name}] Acc: {res.accuracy:.4f} | F1: {res.f1_weighted:.4f} | Zero-Day F1: {res.zero_day_f1:.4f}")

    # Print Ablation Summary Table
    logger.info("\n" + "=" * 80)
    logger.info(f"{'Ablation Configuration':<28} | {'Features':<8} | {'Accuracy':<8} | {'Weighted F1':<11} | {'Zero-Day F1':<11}")
    logger.info("=" * 80)
    for r in ablation_results:
        logger.info(f"{r['config']:<28} | {r['feature_count']:<8} | {r['accuracy']:<8.4f} | {r['f1_weighted']:<11.4f} | {r['zero_day_f1']:<11.4f}")
    logger.info("=" * 80)

    out_file = RESULTS_DIR / "ablation_study_results.json"
    with open(out_file, "w") as f:
        json.dump(ablation_results, f, indent=4)
    logger.info(f"Saved ablation study results to {out_file}")

if __name__ == "__main__":
    run_ablation_study()
