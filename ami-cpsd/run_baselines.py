"""
Baseline Machine Learning & Deep Learning Benchmarking Script for AMI-CPSD v1.0.
Evaluates Logistic Regression, Random Forest, LightGBM, Extra Trees, MLP, and Zero-Day Anomaly Detection.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    base_dir = Path(__file__).resolve().parent
    datasets_dir = base_dir / "datasets"
    results_dir = base_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    train_path = datasets_dir / "train.csv"
    test_path = datasets_dir / "test.csv"
    zero_day_path = datasets_dir / "zero_day_test.csv"

    if not train_path.exists():
        logger.error("Dataset files not found. Run generate_dataset.py first!")
        return

    logger.info("Loading AMI-CPSD v1.0 dataset splits for benchmarking...")
    # Load sample subset for fast benchmarking if dataset is large
    sample_train = 50000
    sample_test = 10000

    df_train = pd.read_csv(train_path, nrows=sample_train)
    df_test = pd.read_csv(test_path, nrows=sample_test)
    df_zero_day = pd.read_csv(zero_day_path, nrows=sample_test)

    # Feature selection (drop text metadata and labels)
    meta_label_cols = [
        "timestamp",
        "meter_id",
        "substation_id",
        "feeder_id",
        "transformer_id",
        "nan_id",
        "dc_id",
        "validator_group",
        "location",
        "consumer_type",
        "grid_state",
        "consensus_protocol",
        "attack_type",
        "attack_category",
        "attack_domain",
        "attack_severity",
        "attack_stage",
        "affected_features",
        "is_attack",
    ]

    feature_cols = [c for c in df_train.columns if c not in meta_label_cols]

    X_train = df_train[feature_cols].copy()
    y_train = df_train["attack_type"].values

    X_test = df_test[feature_cols].copy()
    y_test = df_test["attack_type"].values

    X_zero_day = df_zero_day[feature_cols].copy()
    y_zero_day = df_zero_day["is_attack"].values  # Binary zero day evaluation

    # Impute missing NaNs with mean and scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(imputer.fit_transform(X_train))
    X_test_scaled = scaler.transform(imputer.transform(X_test))
    X_zero_day_scaled = scaler.transform(imputer.transform(X_zero_day))

    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        "Extra Trees": ExtraTreesClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        "Multi-Layer Perceptron (MLP)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42),
    }

    benchmark_results = {}

    logger.info("Evaluating Baseline Machine Learning Models...")
    print("\n" + "=" * 90)
    print(f"{'Model':<30} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'Latency (ms)':<12}")
    print("=" * 90)

    for name, model in models.items():
        # Train
        t0 = time.time()
        model.fit(X_train_scaled, y_train)
        train_time = time.time() - t0

        # Test Inference
        t1 = time.time()
        preds = model.predict(X_test_scaled)
        infer_time = time.time() - t1
        latency_ms_per_sample = (infer_time / len(X_test_scaled)) * 1000.0

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average="weighted", zero_division=0)
        rec = recall_score(y_test, preds, average="weighted", zero_division=0)
        f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

        # Zero-Day Binary Detection Performance
        zero_day_preds = model.predict(X_zero_day_scaled)
        zero_day_binary = (zero_day_preds != 0).astype(int)
        zero_day_f1 = f1_score(y_zero_day, zero_day_binary, average="binary")

        benchmark_results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "zero_day_f1": round(float(zero_day_f1), 4),
            "train_time_sec": round(float(train_time), 2),
            "latency_ms_per_sample": round(float(latency_ms_per_sample), 4),
        }

        print(f"{name:<30} | {acc:<10.4f} | {prec:<10.4f} | {rec:<10.4f} | {f1:<10.4f} | {latency_ms_per_sample:<12.4f}")

    print("=" * 90 + "\n")

    # Save benchmark results
    out_json = results_dir / "benchmark_results.json"
    with open(out_json, "w") as f:
        json.dump(benchmark_results, f, indent=4)

    logger.info(f"Benchmark results successfully saved to {out_json}")


if __name__ == "__main__":
    main()
