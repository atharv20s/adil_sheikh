"""
Evaluation Module for AMI-CPSD v2.0.
Contains classification metrics, confusion matrix helpers, and optional SHAP feature importance.
"""

import json
from pathlib import Path
from typing import Dict, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score


def evaluate_classifier_performance(
    model: Any, X_test: np.ndarray, y_test: np.ndarray, model_name: str
) -> Dict[str, float]:
    """Computes standard classification metrics."""
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average="weighted", zero_division=0)
    rec = recall_score(y_test, preds, average="weighted", zero_division=0)
    f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

    return {
        "model_name": model_name,
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
    }


def save_confusion_matrix_plot(
    y_true: np.ndarray, y_pred: np.ndarray, labels: list, output_path: Path
):
    """Generates confusion matrix plot."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Multi-Class Attack Confusion Matrix", fontsize=12, fontweight="bold")
    ax.set_ylabel("True Category")
    ax.set_xlabel("Predicted Category")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
