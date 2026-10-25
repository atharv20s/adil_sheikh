"""
AMI-CPSD v2.0 Comprehensive Verification & Evidence Report.
Produces auditable evidence for every claim: row counts, class distributions,
physics validation errors, missing data percentages, feature statistics,
leakage checks, temporal continuity, and data type verification.
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = Path(__file__).resolve().parent
DATASETS_DIR = BASE_DIR / "datasets"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def section(title: str):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}")


def main():
    # =========================================================================
    # 1. ROW COUNT VERIFICATION
    # =========================================================================
    section("1. ROW COUNT VERIFICATION")
    expected_counts = {
        "train.csv": 700_000,
        "validation.csv": 150_000,
        "test.csv": 150_000,
        "zero_day_test.csv": 100_000,
    }
    total_actual = 0
    for fname, expected in expected_counts.items():
        fpath = DATASETS_DIR / fname
        if not fpath.exists():
            print(f"  [MISSING] {fname}")
            continue
        # Count lines (subtract 1 for header)
        with open(fpath, "r") as f:
            actual = sum(1 for _ in f) - 1
        total_actual += actual
        status = "PASS" if actual == expected else "FAIL"
        print(f"  [{status}] {fname}: {actual:>10,} rows (expected {expected:,})")

    print(f"\n  Total rows across all splits: {total_actual:,}")
    print(f"  Expected total:               1,100,000")
    print(f"  Match: {'YES' if total_actual == 1_100_000 else 'NO'}")

    # =========================================================================
    # 2. CLASS DISTRIBUTION PER SPLIT
    # =========================================================================
    section("2. CLASS DISTRIBUTION PER SPLIT")
    for fname in expected_counts.keys():
        fpath = DATASETS_DIR / fname
        if not fpath.exists():
            continue
        df = pd.read_csv(fpath, usecols=["attack_category"])
        counts = df["attack_category"].value_counts()
        total = len(df)
        print(f"\n  --- {fname} ({total:,} rows) ---")
        for cat, cnt in counts.items():
            pct = cnt / total * 100.0
            print(f"    {cat:<24}: {cnt:>8,}  ({pct:>5.2f}%)")

    # =========================================================================
    # 3. ZERO-DAY ISOLATION VERIFICATION (HARD CHECK)
    # =========================================================================
    section("3. ZERO-DAY ISOLATION VERIFICATION")
    zero_day_classes = {"Firmware Attack", "Insider Attack", "Malware"}

    for fname in ["train.csv", "validation.csv", "test.csv"]:
        fpath = DATASETS_DIR / fname
        if not fpath.exists():
            continue
        df = pd.read_csv(fpath, usecols=["attack_category"])
        leaked = df[df["attack_category"].isin(zero_day_classes)]
        count = len(leaked)
        status = "PASS" if count == 0 else "FAIL"
        print(f"  [{status}] {fname}: {count} zero-day attack rows found (must be 0)")

    fpath = DATASETS_DIR / "zero_day_test.csv"
    if fpath.exists():
        df = pd.read_csv(fpath, usecols=["attack_category"])
        zd_count = df[df["attack_category"].isin(zero_day_classes)].shape[0]
        print(f"  [INFO] zero_day_test.csv: {zd_count:,} zero-day attack rows present")

    # =========================================================================
    # 4. MISSING DATA PERCENTAGE REPORT
    # =========================================================================
    section("4. MISSING DATA PERCENTAGE REPORT")
    target_cols = [
        "packet_delay", "packet_loss", "rssi", "cpu_usage",
        "ram_usage", "temperature", "consensus_latency", "drift_score",
    ]
    fpath = DATASETS_DIR / "train.csv"
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=100_000)
        print(f"  Inspecting first 100,000 rows of train.csv:")
        print(f"  {'Column':<24} {'Missing Count':>14} {'Missing %':>10}")
        print(f"  {'-'*50}")
        for col in target_cols:
            if col in df.columns:
                n_miss = df[col].isna().sum()
                pct = n_miss / len(df) * 100.0
                print(f"  {col:<24} {n_miss:>14,} {pct:>9.2f}%")
        total_miss = df[target_cols].isna().sum().sum()
        total_cells = len(df) * len(target_cols)
        print(f"\n  Aggregate missing across target columns: {total_miss:,} / {total_cells:,} ({total_miss/total_cells*100:.2f}%)")

    # =========================================================================
    # 5. PHYSICS VALIDATION REPORT (P = V * I * cos(phi) / 1000)
    # =========================================================================
    section("5. PHYSICS VALIDATION REPORT")
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=100_000)
        normal = df[df["is_attack"] == 0].dropna(subset=["voltage", "current", "power_factor", "active_power"])

        p_calc = (normal["voltage"] * normal["current"] * normal["power_factor"]) / 1000.0
        p_measured = normal["active_power"]
        residual = np.abs(p_calc - p_measured)

        print(f"  Normal samples inspected: {len(normal):,}")
        print(f"  P_calc = (V * I * cos(phi)) / 1000")
        print(f"")
        print(f"  Residual |P_calc - P_measured|:")
        print(f"    Mean:    {residual.mean():.6f} kW")
        print(f"    Median:  {residual.median():.6f} kW")
        print(f"    Max:     {residual.max():.6f} kW")
        print(f"    Std:     {residual.std():.6f} kW")

        within_tolerance = (residual < 0.05).sum()
        pct_within = within_tolerance / len(normal) * 100.0
        print(f"\n  Samples within 0.05 kW tolerance: {within_tolerance:,} / {len(normal):,} ({pct_within:.2f}%)")

        # Also check attack samples (FDI) to confirm they VIOLATE physics
        fdi = df[df["attack_category"] == "False Data Injection"].dropna(subset=["voltage", "current", "power_factor", "active_power"])
        if len(fdi) > 0:
            fdi_p_calc = (fdi["voltage"] * fdi["current"] * fdi["power_factor"]) / 1000.0
            fdi_residual = np.abs(fdi_p_calc - fdi["active_power"])
            print(f"\n  FDI attack samples inspected: {len(fdi):,}")
            print(f"    Mean residual: {fdi_residual.mean():.4f} kW")
            print(f"    Max residual:  {fdi_residual.max():.4f} kW")
            print(f"    (Expected: large residuals confirming physics violation)")

    # =========================================================================
    # 6. FEATURE STATISTICS (DESCRIPTIVE)
    # =========================================================================
    section("6. FEATURE STATISTICS (train.csv, first 100k rows)")
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=100_000)
        numeric_cols = [
            "voltage", "current", "frequency", "active_power", "power_factor",
            "packet_rate", "packet_delay", "cpu_usage", "ram_usage", "temperature",
            "consensus_latency", "anomaly_score", "entropy", "drift_score",
        ]
        stats = df[numeric_cols].describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]]
        print(stats.to_string())

    # =========================================================================
    # 7. DATA TYPE VERIFICATION
    # =========================================================================
    section("7. DATA TYPE VERIFICATION")
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=10)
        print(f"  {'Column':<28} {'Dtype':<16} {'Sample Value'}")
        print(f"  {'-'*60}")
        for col in df.columns:
            print(f"  {col:<28} {str(df[col].dtype):<16} {df[col].iloc[0]}")

    # =========================================================================
    # 8. TEMPORAL CONTINUITY CHECK (OU process smoothness)
    # =========================================================================
    section("8. TEMPORAL CONTINUITY CHECK")
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=1000)
        normal = df[df["is_attack"] == 0].head(200)
        if len(normal) > 10:
            v_diff = normal["voltage"].diff().dropna().abs()
            c_diff = normal["current"].diff().dropna().abs()
            print(f"  Consecutive voltage step |V[t] - V[t-1]| (normal samples, first 200):")
            print(f"    Mean step:  {v_diff.mean():.4f} V")
            print(f"    Max step:   {v_diff.max():.4f} V")
            print(f"    Std step:   {v_diff.std():.4f} V")
            print(f"\n  Consecutive current step |I[t] - I[t-1]| (normal samples, first 200):")
            print(f"    Mean step:  {c_diff.mean():.4f} A")
            big_jumps_v = (v_diff > 10.0).sum()
            big_jumps_c = (c_diff > 15.0).sum()
            print(f"\n  Voltage jumps > 10V: {big_jumps_v} (should be ~0 for OU process)")
            print(f"  Current jumps > 15A: {big_jumps_c} (should be ~0 for OU process)")

            # Additional Physical Integrity Checks
            v_bounded = df["voltage"].between(180.0, 280.0).all()
            e_diff = normal["energy"].diff().dropna()
            monotonic_energy = (e_diff >= -0.01).all()
            max_c_ramp = c_diff.max() <= 25.0

            print(f"\n  Physical Integrity Assertions:")
            print(f"    [{'PASS' if v_bounded else 'FAIL'}] Voltage bounded within 180V-280V")
            print(f"    [{'PASS' if monotonic_energy else 'FAIL'}] Monotonic Energy Accumulation (delta E >= 0)")
            print(f"    [{'PASS' if max_c_ramp else 'FAIL'}] Max Current Ramp <= 25A/step")

    # =========================================================================
    # 9. LABEL LEAKAGE CHECK (CRITICAL)
    # =========================================================================
    section("9. LABEL LEAKAGE CHECK (CRITICAL)")
    print("  Checking whether label-derived columns are separable from training features...")
    print()
    if fpath.exists():
        df = pd.read_csv(fpath, nrows=10)
        label_cols = [
            "attack_type", "attack_category", "attack_domain", "attack_severity",
            "attack_stage", "affected_features", "is_attack", "attack_start",
            "attack_end", "duration_sec", "recovery_time_sec",
        ]
        feature_cols = [c for c in df.columns if c not in label_cols and c not in [
            "timestamp", "meter_id", "substation_id", "feeder_id", "transformer_id",
            "nan_id", "dc_id", "validator_group", "location", "consumer_type",
            "grid_state", "consensus_protocol",
        ]]

        print(f"  Label/metadata columns that MUST NOT be used as training features:")
        for col in label_cols:
            present = col in df.columns
            print(f"    {'[PRESENT]' if present else '[ABSENT]'} {col}")

        print(f"\n  Numeric feature columns available for training ({len(feature_cols)} features):")
        for col in feature_cols:
            print(f"    {col}")

        print(f"\n  [WARNING] LEAKAGE RISK ASSESSMENT:")
        print(f"  If ANY of the label columns above are included in X_train during")
        print(f"  model training, the classifier can trivially 'cheat'.")
        print(f"  The benchmark script (run_experiments.py) explicitly excludes them.")
        print(f"  Verify this in run_experiments.py line: meta_cols = [...]")

    # =========================================================================
    # 10. DATASET FILE INVENTORY
    # =========================================================================
    section("10. DATASET FILE INVENTORY")
    for p in sorted(DATASETS_DIR.iterdir()):
        size_mb = p.stat().st_size / (1024 * 1024)
        print(f"  {p.name:<30} {size_mb:>10.2f} MB")

    print(f"\n{'=' * 80}")
    print(f"  VERIFICATION REPORT COMPLETE")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
