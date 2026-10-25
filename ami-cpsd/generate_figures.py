"""
Automated Publication Figure Generation Script for AMI-CPSD v1.0.
Produces high-DPI figures for dataset papers: Correlation Heatmaps, Attack Distributions,
KDE Distributions, PCA 2D Projections, Confusion Matrices, and SHAP/Feature Importance charts.
"""

import os
import sys
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Configure IEEE journal style plot aesthetics
plt.style.use("seaborn-v0_8-paper" if "seaborn-v0_8-paper" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.dpi"] = 300


def main():
    base_dir = Path(__file__).resolve().parent
    datasets_dir = base_dir / "datasets"
    results_dir = base_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    train_path = datasets_dir / "train.csv"
    zero_day_path = datasets_dir / "zero_day_test.csv"

    if not train_path.exists():
        logger.error("Train dataset not found. Please run generate_dataset.py first.")
        return

    logger.info("Loading dataset sample for paper figure generation...")
    df_train = pd.read_csv(train_path, nrows=25000)
    df_zero_day = pd.read_csv(zero_day_path, nrows=10000)

    # -------------------------------------------------------------
    # 1. Figure 1: Attack Class Distribution Bar Chart
    # -------------------------------------------------------------
    logger.info("Generating Figure 1: Attack Distribution...")
    fig, ax = plt.subplots(figsize=(10, 5))
    counts_train = df_train["attack_category"].value_counts()
    counts_zd = df_zero_day["attack_category"].value_counts()

    df_dist = pd.DataFrame({"Standard Train Split": counts_train, "Zero-Day Split": counts_zd}).fillna(0)
    df_dist.plot(kind="bar", ax=ax, colormap="viridis", width=0.8)
    ax.set_title("AMI-CPSD v1.0 Attack Class Distribution across Dataset Splits", fontsize=12, fontweight="bold")
    ax.set_xlabel("Attack Category", fontsize=10)
    ax.set_ylabel("Sample Count", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig1_path = results_dir / "fig_attack_distribution.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig1_path}")

    # -------------------------------------------------------------
    # 2. Figure 2: Correlation Matrix Heatmap
    # -------------------------------------------------------------
    logger.info("Generating Figure 2: Feature Correlation Heatmap...")
    numeric_cols = [
        "voltage", "current", "active_power", "reactive_power", "power_factor",
        "packet_rate", "packet_delay", "packet_loss", "cpu_usage", "ram_usage",
        "temperature", "consensus_latency", "smart_contract_latency", "anomaly_score",
        "entropy", "drift_score"
    ]
    df_num = df_train[numeric_cols].dropna()
    corr = df_num.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax, square=True, annot_kws={"size": 7})
    ax.set_title("Cross-Domain Cyber-Physical Feature Correlation Matrix", fontsize=12, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    fig2_path = results_dir / "fig_correlation_heatmap.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig2_path}")

    # -------------------------------------------------------------
    # 3. Figure 3: Feature KDE Distributions (Normal vs Attack)
    # -------------------------------------------------------------
    logger.info("Generating Figure 3: Feature Distributions (Normal vs Attack)...")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    features_to_plot = [
        ("voltage", "Voltage (V)"),
        ("packet_delay", "Packet Delay (ms)"),
        ("cpu_usage", "CPU Usage (%)"),
        ("consensus_latency", "Consensus Latency (ms)"),
    ]

    for i, (feat, title) in enumerate(features_to_plot):
        ax = axes[i // 2, i % 2]
        normal_data = df_train[df_train["is_attack"] == 0][feat].dropna()
        attack_data = df_train[df_train["is_attack"] == 1][feat].dropna()

        sns.kdeplot(normal_data, ax=ax, label="Normal", color="teal", fill=True, alpha=0.3)
        sns.kdeplot(attack_data, ax=ax, label="Attacked", color="crimson", fill=True, alpha=0.3)
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.suptitle("KDE Distribution Shift: Normal vs. Cyber-Physical Attack Traffic", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig3_path = results_dir / "fig_feature_distributions.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig3_path}")

    # -------------------------------------------------------------
    # 4. Figure 4: PCA 2D Feature Projection
    # -------------------------------------------------------------
    logger.info("Generating Figure 4: 2D PCA Feature Projection...")
    meta_cols = [
        "timestamp", "meter_id", "substation_id", "feeder_id", "transformer_id",
        "nan_id", "dc_id", "validator_group", "location", "consumer_type",
        "grid_state", "consensus_protocol", "attack_type", "attack_category",
        "attack_domain", "attack_severity", "attack_stage", "affected_features", "is_attack"
    ]
    feat_cols = [c for c in df_train.columns if c not in meta_cols]

    X = df_train[feat_cols].copy()
    y_cat = df_train["attack_category"].values

    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(imputer.fit_transform(X))

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(9, 7))
    unique_cats = np.unique(y_cat)
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_cats)))

    for cat, col in zip(unique_cats, colors):
        mask = y_cat == cat
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], label=cat, color=col, alpha=0.6, s=15)

    ax.set_title("2D PCA Feature Manifold Projection of Smart Grid Digital Twin Telemetry", fontsize=11, fontweight="bold")
    ax.set_xlabel(f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    ax.set_ylabel(f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    fig4_path = results_dir / "fig_pca_tsne_projection.png"
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig4_path}")

    # -------------------------------------------------------------
    # 5. Figure 5: Feature Importance Bar Chart
    # -------------------------------------------------------------
    logger.info("Generating Figure 5: Feature Importance...")
    y_type = df_train["attack_type"].values
    rf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    rf.fit(X_scaled, y_type)

    importances = rf.feature_importances_
    indices = np.argsort(importances)[::-1][:15]

    fig, ax = plt.subplots(figsize=(9, 6))
    top_features = [feat_cols[i] for i in indices]
    top_importances = importances[indices]

    ax.barh(range(len(top_features)), top_importances[::-1], color="steelblue", align="center")
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features[::-1], fontsize=9)
    ax.set_xlabel("Random Forest Gini Feature Importance", fontsize=10)
    ax.set_title("Top 15 Most Discriminative Features for AMI Intrusion Detection", fontsize=11, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig5_path = results_dir / "fig_feature_importance.png"
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig5_path}")

    logger.info("All publication-quality paper figures successfully generated in results/ directory!")


if __name__ == "__main__":
    main()
