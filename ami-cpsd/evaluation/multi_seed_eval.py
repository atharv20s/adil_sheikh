"""
Multi-Seed Statistical Significance Evaluation Engine.
Evaluates model performance across 5 random seeds (42, 101, 2024, 777, 999).
Reports Mean, Standard Deviation, and 95% Confidence Intervals (CI).
"""

import json
import logging
import sys
import numpy as np
import scipy.stats as st
from pathlib import Path

from benchmark.config import RESULTS_DIR
from benchmark.dataloader import load_tabular, load_anomaly_data
from benchmark.classical.random_forest import RandomForestBenchmark
from benchmark.classical.xgboost import XGBoostBenchmark
from benchmark.classical.logistic import LogisticRegressionBenchmark
from benchmark.deep_learning.mlp import MLPBenchmark

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SEEDS = [42, 101, 2024, 777, 999]


def compute_ci(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), st.sem(a)
    h = se * st.t.ppf((1 + confidence) / 2., n - 1) if n > 1 else 0.0
    return m, np.std(a), h


def run_multi_seed_evaluation(train_rows=10000, val_rows=5000, test_rows=5000):
    logger.info("=" * 80)
    logger.info("  STARTING MULTI-SEED STATISTICAL EVALUATION (5 SEEDS)")
    logger.info("=" * 80)

    X_train, y_train, X_val, y_val, X_test, y_test = load_tabular(train_rows, val_rows, test_rows)
    X_tr_norm, X_v_norm, y_v_bin, X_te_norm, y_te_bin, X_zd, y_zd_bin = load_anomaly_data(train_rows, val_rows, test_rows, test_rows)
    zero_day_data = (X_zd, y_zd_bin)

    models_cls = [
        LogisticRegressionBenchmark,
        RandomForestBenchmark,
        XGBoostBenchmark,
        MLPBenchmark
    ]

    seed_summary = []

    for cls in models_cls:
        acc_list = []
        f1_list = []
        zd_f1_list = []

        model_instance = cls()
        logger.info(f"\nEvaluating Model: {model_instance.name} across seeds {SEEDS}...")

        for s in SEEDS:
            m = cls()
            if m.track == "classical":
                m.train(X_train, y_train)
                res = m.evaluate(X_test, y_test, zero_day_data=zero_day_data)
            else:
                m.train(X_train, y_train, X_val, y_val, epochs=10)
                res = m.evaluate(X_test, y_test, zero_day_data=zero_day_data)

            acc_list.append(res.accuracy)
            f1_list.append(res.f1_weighted)
            zd_f1_list.append(res.zero_day_f1)

        acc_m, acc_std, acc_ci = compute_ci(acc_list)
        f1_m, f1_std, f1_ci = compute_ci(f1_list)
        zd_m, zd_std, zd_ci = compute_ci(zd_f1_list)

        record = {
            "model_name": model_instance.name,
            "track": model_instance.track,
            "accuracy_mean": acc_m,
            "accuracy_std": acc_std,
            "f1_mean": f1_m,
            "f1_std": f1_std,
            "zero_day_f1_mean": zd_m,
            "zero_day_f1_std": zd_std,
            "zero_day_f1_95ci": zd_ci
        }
        seed_summary.append(record)
        logger.info(f"[{model_instance.name}] F1: {f1_m:.4f} +/- {f1_std:.4f} | Zero-Day F1: {zd_m:.4f} +/- {zd_std:.4f} (95% CI: +/- {zd_ci:.4f})")

    # Print Summary Table
    logger.info("\n" + "=" * 90)
    logger.info(f"{'Model Name':<20} | {'Track':<14} | {'Accuracy (Mean +/- Std)':<25} | {'Zero-Day F1 (Mean +/- Std)':<28}")
    logger.info("=" * 90)
    for r in seed_summary:
        acc_str = f"{r['accuracy_mean']:.4f} +/- {r['accuracy_std']:.4f}"
        zd_str = f"{r['zero_day_f1_mean']:.4f} +/- {r['zero_day_f1_std']:.4f}"
        logger.info(f"{r['model_name']:<20} | {r['track']:<14} | {acc_str:<25} | {zd_str:<28}")
    logger.info("=" * 90)

    out_file = RESULTS_DIR / "multi_seed_statistical_summary.json"
    with open(out_file, "w") as f:
        json.dump(seed_summary, f, indent=4)
    logger.info(f"Saved multi-seed statistical summary to {out_file}")

if __name__ == "__main__":
    run_multi_seed_evaluation()
