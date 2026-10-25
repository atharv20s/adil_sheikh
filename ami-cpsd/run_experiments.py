"""
AMI-CPSD v2.0 Benchmark Runner with Full Experimental Logs.
Produces auditable training output, confusion matrices, and per-class metrics.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Columns that MUST be excluded from features to prevent leakage
EXCLUDED_COLS = [
    "timestamp", "meter_id", "substation_id", "feeder_id", "transformer_id",
    "nan_id", "dc_id", "validator_group", "location", "consumer_type",
    "grid_state", "consensus_protocol",
    # ALL label columns
    "attack_type", "attack_category", "attack_domain", "attack_severity",
    "attack_stage", "affected_features", "is_attack",
    "attack_start", "attack_end", "duration_sec", "recovery_time_sec",
]


def main():
    train_path = DATASETS_DIR / "train.csv"
    test_path = DATASETS_DIR / "test.csv"
    zero_day_path = DATASETS_DIR / "zero_day_test.csv"

    if not train_path.exists():
        logger.error("Datasets not found.")
        return

    # Load data
    sample_n = 50_000
    logger.info(f"Loading {sample_n:,} rows from each split...")
    df_train = pd.read_csv(train_path, nrows=sample_n)
    df_test = pd.read_csv(test_path, nrows=10_000)
    df_zero_day = pd.read_csv(zero_day_path, nrows=10_000)

    feature_cols = [c for c in df_train.columns if c not in EXCLUDED_COLS]

    print("\n" + "=" * 80)
    print("  FEATURE COLUMNS USED FOR TRAINING (Leakage Check)")
    print("=" * 80)
    for i, col in enumerate(feature_cols):
        print(f"  {i+1:>2}. {col}")
    print(f"\n  Total features: {len(feature_cols)}")
    print(f"  Excluded columns: {len(EXCLUDED_COLS)}")

    X_train = df_train[feature_cols].copy()
    y_train = df_train["attack_type"].values
    X_test = df_test[feature_cols].copy()
    y_test = df_test["attack_type"].values
    X_zd = df_zero_day[feature_cols].copy()
    y_zd_binary = df_zero_day["is_attack"].values

    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(imputer.fit_transform(X_train))
    X_test_s = scaler.transform(imputer.transform(X_test))
    X_zd_s = scaler.transform(imputer.transform(X_zd))

    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=15, random_state=42, n_jobs=-1
        ),
        "Multi-Layer Perceptron (MLP)": MLPClassifier(
            hidden_layer_sizes=(64, 32), max_iter=200, random_state=42
        ),
    }

    all_results = {}

    for name, model in models.items():
        print("\n" + "=" * 80)
        print(f"  MODEL: {name}")
        print("=" * 80)

        t0 = time.time()
        model.fit(X_train_s, y_train)
        train_time = time.time() - t0
        print(f"  Training time: {train_time:.2f} seconds")

        # --- Standard test evaluation ---
        t1 = time.time()
        preds = model.predict(X_test_s)
        infer_time = time.time() - t1
        latency_ms = (infer_time / len(X_test_s)) * 1000.0

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average="weighted", zero_division=0)
        rec = recall_score(y_test, preds, average="weighted", zero_division=0)
        f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

        print(f"\n  --- Standard Test Set (test.csv, {len(X_test_s):,} rows) ---")
        print(f"  Accuracy:   {acc:.4f}")
        print(f"  Precision:  {prec:.4f}  (weighted)")
        print(f"  Recall:     {rec:.4f}  (weighted)")
        print(f"  F1-Score:   {f1:.4f}  (weighted)")
        print(f"  Inference:  {infer_time*1000:.2f} ms total, {latency_ms:.4f} ms/sample")

        print(f"\n  Per-Class Classification Report:")
        report = classification_report(y_test, preds, zero_division=0)
        print(report)

        print(f"  Confusion Matrix:")
        cm = confusion_matrix(y_test, preds)
        # Get sorted unique labels from both true and predicted
        all_labels = sorted(set(y_test) | set(preds))
        header = "       " + "  ".join(f"{l:>5}" for l in all_labels)
        print(header)
        for i, row in enumerate(cm):
            print(f"  {all_labels[i]:>4} | " + "  ".join(f"{v:>5}" for v in row))

        # --- Zero-Day binary evaluation ---
        zd_preds = model.predict(X_zd_s)
        zd_binary_preds = (zd_preds != 0).astype(int)
        zd_acc = accuracy_score(y_zd_binary, zd_binary_preds)
        zd_f1 = f1_score(y_zd_binary, zd_binary_preds, average="binary")

        print(f"\n  --- Zero-Day Detection (zero_day_test.csv, Binary) ---")
        print(f"  Accuracy:   {zd_acc:.4f}")
        print(f"  F1-Score:   {zd_f1:.4f}")

        all_results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "train_time_sec": round(train_time, 2),
            "latency_ms_per_sample": round(latency_ms, 4),
            "zero_day_accuracy": round(float(zd_acc), 4),
            "zero_day_f1": round(float(zd_f1), 4),
        }

    out_path = RESULTS_DIR / "benchmark_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\n{'=' * 80}")
    print(f"  Benchmark results saved to {out_path}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
