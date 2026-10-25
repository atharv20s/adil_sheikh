"""
Evaluation and Metrics Compilation Module for AMI-CPSD v2.0.
Provides standardized evaluation routines, confusion matrix plotting,
ROC/PR calculations, and zero-day anomaly checks.
"""

import json
import time
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc, confusion_matrix,
    classification_report
)

from benchmark.config import FIGURES_DIR, REPORTS_DIR

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    model_name: str
    track: str
    accuracy: float
    precision_weighted: float
    recall_weighted: float
    f1_weighted: float
    roc_auc_macro: float
    pr_auc_macro: float
    train_time_sec: float
    inference_latency_ms: float
    zero_day_accuracy: float
    zero_day_f1: float


def plot_confusion_matrix(y_true, y_pred, labels, model_name):
    """Saves a styled confusion matrix heatmap to figures directory."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=labels, yticklabels=labels, cbar=True
    )
    plt.title(f"Confusion Matrix: {model_name}", fontsize=12, fontweight="bold")
    plt.ylabel("True Class")
    plt.xlabel("Predicted Class")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    out_path = FIGURES_DIR / f"cm_{model_name.lower().replace(' ', '_')}.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved confusion matrix to {out_path}")


def evaluate_model(
    model, X_test, y_test, model_name, track, train_time,
    y_test_probs=None, is_pytorch=False, sequence_input=False,
    zero_day_data=None, is_anomaly=False
):
    """
    Evaluates classification models (multiclass) and zero-day anomaly detectors (binary).
    Measures latency, accuracy, weighted and macro curves.
    """
    logger.info(f"Evaluating {model_name}...")
    
    # 1. Inference Latency & Predictions
    t0 = time.time()
    if is_pytorch:
        import torch
        model.eval()
        with torch.no_grad():
            if sequence_input:
                # Expects a PyTorch Dataloader
                preds_list = []
                probs_list = []
                for x_batch, _ in X_test:
                    outputs = model(x_batch)
                    if isinstance(outputs, tuple):
                        outputs = outputs[0]
                    probs = torch.softmax(outputs, dim=1)
                    preds = torch.argmax(outputs, dim=1)
                    preds_list.append(preds.cpu().numpy())
                    probs_list.append(probs.cpu().numpy())
                y_pred = np.concatenate(preds_list)
                y_prob = np.concatenate(probs_list)
                num_samples = len(y_pred)
            else:
                x_tensor = torch.tensor(X_test, dtype=torch.float32)
                outputs = model(x_tensor)
                if isinstance(outputs, tuple):
                    outputs = outputs[0]
                y_prob = torch.softmax(outputs, dim=1).numpy()
                y_pred = torch.argmax(outputs, dim=1).numpy()
                num_samples = len(X_test)
    elif is_anomaly:
        # Anomaly detectors (Autoencoder / Isolation Forest)
        if hasattr(model, "threshold"):  # Autoencoder
            import torch
            model.eval()
            with torch.no_grad():
                x_tensor = torch.tensor(X_test, dtype=torch.float32)
                recon = model(x_tensor)
                mse = torch.mean((x_tensor - recon) ** 2, dim=1).cpu().numpy()
                y_pred_binary = (mse > model.threshold).astype(int)
            num_samples = len(X_test)
        else:  # Isolation Forest
            # IF predicts -1 for anomaly, 1 for normal
            if_preds = model.predict(X_test)
            y_pred_binary = (if_preds == -1).astype(int)
            num_samples = len(X_test)
        y_pred = None
        y_prob = None
    else:
        # Standard scikit-learn / Boosting API
        y_pred = model.predict(X_test)
        y_prob = y_test_probs if y_test_probs is not None else model.predict_proba(X_test)
        num_samples = len(X_test)

    elapsed_infer = time.time() - t0
    latency = (elapsed_infer / num_samples) * 1000.0 if num_samples > 0 else 0.0

    # 2. Compute standard multiclass metrics
    acc = 0.0
    prec = 0.0
    rec = 0.0
    f1 = 0.0
    roc_auc = 0.0
    pr_auc = 0.0

    if not is_anomaly:
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        # ROC / PR curves
        unique_classes = np.unique(y_test)
        num_classes = len(unique_classes)
        
        # Determine class to column mapping for sklearn models
        if hasattr(model, "classes_"):
            class_to_col = {cls: idx for idx, cls in enumerate(model.classes_)}
        else:
            class_to_col = {cls: cls for cls in unique_classes}

        # Calculate Multi-Class ROC AUC (OVR)
        try:
            if hasattr(model, "classes_"):
                roc_auc = roc_auc_score(y_test, y_prob, labels=model.classes_, multi_class="ovr", average="macro")
            else:
                roc_auc = roc_auc_score(y_test, y_prob, multi_class="ovr", average="macro")
        except Exception:
            roc_auc = 0.0

        # Calculate PR AUC using One-vs-Rest macro-average manual compile
        pr_aucs = []
        for c in unique_classes:
            y_true_c = (y_test == c).astype(int)
            if y_prob is not None and c in class_to_col:
                col_idx = class_to_col[c]
                if col_idx < y_prob.shape[1]:
                    y_prob_c = y_prob[:, col_idx]
                else:
                    y_prob_c = (y_pred == c).astype(int)
            else:
                y_prob_c = (y_pred == c).astype(int)
            precision_c, recall_c, _ = precision_recall_curve(y_true_c, y_prob_c)
            pr_aucs.append(auc(recall_c, precision_c))
        pr_auc = np.mean(pr_aucs) if pr_aucs else 0.0

        # Save classification report txt
        rep = classification_report(y_test, y_pred, zero_division=0)
        report_file = REPORTS_DIR / f"{model_name.lower().replace(' ', '_')}.txt"
        with open(report_file, "w") as f:
            f.write(f"Model: {model_name}\nTrack: {track}\n\n")
            f.write(rep)

        # Plot confusion matrix
        labels = [str(c) for c in unique_classes]
        plot_confusion_matrix(y_test, y_pred, labels, model_name)
    else:
        # Anomaly detection standard testing is evaluated as binary (Normal vs Attack)
        # Note: Standard y_test needs to be converted to binary
        y_test_binary = (y_test != 0).astype(int) if len(y_test.shape) == 1 else y_test
        acc = accuracy_score(y_test_binary, y_pred_binary)
        prec = precision_score(y_test_binary, y_pred_binary, average="binary", zero_division=0)
        rec = recall_score(y_test_binary, y_pred_binary, average="binary")
        f1 = f1_score(y_test_binary, y_pred_binary, average="binary", zero_division=0)
        
        # Save simple report
        rep = classification_report(y_test_binary, y_pred_binary, zero_division=0)
        report_file = REPORTS_DIR / f"{model_name.lower().replace(' ', '_')}.txt"
        with open(report_file, "w") as f:
            f.write(f"Anomaly Model: {model_name}\nTrack: {track}\n\n")
            f.write(rep)
        
        plot_confusion_matrix(y_test_binary, y_pred_binary, ["Normal", "Anomaly"], model_name)

    # 3. Evaluate Zero-Day (zero_day_test.csv)
    zd_acc = 0.0
    zd_f1 = 0.0
    if zero_day_data is not None:
        if sequence_input:
            zd_loader, y_zd_binary = zero_day_data
            import torch
            model.eval()
            preds_list = []
            with torch.no_grad():
                for x_batch, _ in zd_loader:
                    outputs = model(x_batch)
                    if isinstance(outputs, tuple):
                        outputs = outputs[0]
                    preds = torch.argmax(outputs, dim=1).cpu().numpy()
                    preds_list.append(preds)
            multiclass_preds = np.concatenate(preds_list)
            zd_preds = (multiclass_preds != 0).astype(int)
        else:
            X_zd, y_zd_binary = zero_day_data
            if is_anomaly:
                if hasattr(model, "threshold"):  # AE
                    import torch
                    model.eval()
                    with torch.no_grad():
                        zd_tensor = torch.tensor(X_zd, dtype=torch.float32)
                        recon = model(zd_tensor)
                        mse = torch.mean((zd_tensor - recon) ** 2, dim=1).cpu().numpy()
                        zd_preds = (mse > model.threshold).astype(int)
                else:  # IF
                    if_preds = model.predict(X_zd)
                    zd_preds = (if_preds == -1).astype(int)
            else:
                if is_pytorch:
                    import torch
                    model.eval()
                    with torch.no_grad():
                        zd_tensor = torch.tensor(X_zd, dtype=torch.float32)
                        outputs = model(zd_tensor)
                        if isinstance(outputs, tuple):
                            outputs = outputs[0]
                        multiclass_preds = torch.argmax(outputs, dim=1).cpu().numpy()
                else:
                    multiclass_preds = model.predict(X_zd)
                zd_preds = (multiclass_preds != 0).astype(int)

        zd_acc = accuracy_score(y_zd_binary, zd_preds)
        zd_f1 = f1_score(y_zd_binary, zd_preds, average="binary", zero_division=0)

    # Compile result object
    res = BenchmarkResult(
        model_name=model_name,
        track=track,
        accuracy=round(acc, 4),
        precision_weighted=round(prec, 4),
        recall_weighted=round(rec, 4),
        f1_weighted=round(f1, 4),
        roc_auc_macro=round(roc_auc, 4),
        pr_auc_macro=round(pr_auc, 4),
        train_time_sec=round(train_time, 2),
        inference_latency_ms=round(latency, 6),
        zero_day_accuracy=round(zd_acc, 4),
        zero_day_f1=round(zd_f1, 4)
    )

    logger.info(
        f"[{model_name}] F1: {res.f1_weighted:.4f} | "
        f"Zero-Day F1: {res.zero_day_f1:.4f} | Latency: {res.inference_latency_ms:.4f} ms/sample"
    )
    return res
