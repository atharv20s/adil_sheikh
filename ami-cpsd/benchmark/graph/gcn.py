"""
Graph Convolutional Network (GCN) Benchmark Model for Track 3 (GNNs).
Conditional implementation that handles absence of torch_geometric gracefully.
"""

import time
import logging
import numpy as np
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.evaluator import BenchmarkResult, evaluate_model, plot_confusion_matrix

logger = logging.getLogger(__name__)

# Conditional import
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch_geometric.nn import GCNConv
    from torch_geometric.loader import DataLoader as PyGDataLoader
    PYG_AVAILABLE = True
except ImportError:
    PYG_AVAILABLE = False


if PYG_AVAILABLE:
    class GCNNet(nn.Module):
        def __init__(self, input_dim=52, hidden_dim=128, num_classes=13):
            super().__init__()
            self.conv1 = GCNConv(input_dim, hidden_dim)
            self.conv2 = GCNConv(hidden_dim, 64)
            self.fc = nn.Linear(64, num_classes)

        def forward(self, data):
            x, edge_index = data.x, data.edge_index
            x = self.conv1(x, edge_index).relu()
            x = nn.functional.dropout(x, p=0.3, training=self.training)
            x = self.conv2(x, edge_index).relu()
            return self.fc(x)


class GCNBenchmark(BenchmarkModel):
    def __init__(self, input_dim=52, num_classes=13):
        super().__init__(name="GCN", track="graph")
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.model = self.get_model()
        self.train_time = 0.0

    def get_model(self):
        if not PYG_AVAILABLE:
            return None
        return GCNNet(input_dim=self.input_dim, num_classes=self.num_classes)

    def train(self, train_snapshots, val_snapshots=None, epochs=20, lr=0.001, batch_size=32, device="cpu"):
        if not PYG_AVAILABLE:
            logger.warning("PyG not installed. Skipping GCN training.")
            return 0.0

        logger.info(f"Training GCN node classifier on {device}...")
        self.model = self.model.to(device)
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        train_loader = PyGDataLoader(train_snapshots, batch_size=batch_size, shuffle=True)
        
        t0 = time.time()
        for epoch in range(1, epochs + 1):
            self.model.train()
            epoch_loss = 0.0
            for batch in train_loader:
                batch = batch.to(device)
                optimizer.zero_grad()
                out = self.model(batch)
                loss = criterion(out, batch.y)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * batch.num_graphs
            epoch_loss /= len(train_snapshots)
            if epoch % 5 == 0 or epoch == 1:
                logger.info(f"GCN Epoch {epoch}/{epochs} - Loss: {epoch_loss:.4f}")

        self.train_time = time.time() - t0
        logger.info(f"GCN training completed in {self.train_time:.2f} seconds.")
        return self.train_time

    def predict(self, batch, device="cpu"):
        if not PYG_AVAILABLE:
            return None
        self.model.eval()
        self.model.to(device)
        with torch.no_grad():
            batch = batch.to(device)
            out = self.model(batch)
            return torch.argmax(out, dim=1).cpu().numpy()

    def evaluate(self, test_snapshots, y_test=None, zero_day_data=None):
        """
        Evaluates the node classifier across all test snapshots.
        """
        if not PYG_AVAILABLE:
            # Return dummy result if PyG not installed
            return BenchmarkResult(
                model_name=self.name, track=self.track,
                accuracy=0.0, precision_weighted=0.0, recall_weighted=0.0, f1_weighted=0.0,
                roc_auc_macro=0.0, pr_auc_macro=0.0, train_time_sec=0.0, inference_latency_ms=0.0,
                zero_day_accuracy=0.0, zero_day_f1=0.0
            )

        logger.info("Evaluating GCN node classifier...")
        self.model.eval()
        
        test_loader = PyGDataLoader(test_snapshots, batch_size=32, shuffle=False)
        
        preds_list = []
        true_list = []
        
        t0 = time.time()
        with torch.no_grad():
            for batch in test_loader:
                out = self.model(batch)
                preds = torch.argmax(out, dim=1)
                preds_list.append(preds.cpu().numpy())
                true_list.append(batch.y.cpu().numpy())
        
        elapsed = time.time() - t0
        y_pred = np.concatenate(preds_list)
        y_true = np.concatenate(true_list)
        
        num_samples = len(y_true)
        latency = (elapsed / num_samples) * 1000.0 if num_samples > 0 else 0.0

        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

        # Plot confusion matrix
        unique_classes = np.unique(y_true)
        plot_confusion_matrix(y_true, y_pred, [str(c) for c in unique_classes], self.name)

        # Evaluate Zero-Day (unseen attack node binary mapping)
        # For simplicity, if node is not Normal (class != 0) it is an anomaly
        zd_acc = 0.0
        zd_f1 = 0.0
        if zero_day_data is not None:
            # zero_day_data is a tuple of (X_zd, y_zd_binary) or list of zero-day snapshots.
            # If it's snapshots:
            if isinstance(zero_day_data, list):
                zd_loader = PyGDataLoader(zero_day_data, batch_size=32, shuffle=False)
                zd_preds_list = []
                zd_true_list = []
                with torch.no_grad():
                    for batch in zd_loader:
                        out = self.model(batch)
                        preds = torch.argmax(out, dim=1)
                        zd_preds_list.append(preds.cpu().numpy())
                        zd_true_list.append(batch.y.cpu().numpy())
                zd_pred_binary = (np.concatenate(zd_preds_list) != 0).astype(int)
                zd_true_binary = (np.concatenate(zd_true_list) != 0).astype(int)
                
                zd_acc = accuracy_score(zd_true_binary, zd_pred_binary)
                zd_f1 = f1_score(zd_true_binary, zd_pred_binary, average="binary", zero_division=0)

        res = BenchmarkResult(
            model_name=self.name,
            track=self.track,
            accuracy=round(acc, 4),
            precision_weighted=round(prec, 4),
            recall_weighted=round(rec, 4),
            f1_weighted=round(f1, 4),
            roc_auc_macro=0.0, # Not computed for graph nodes multi-class for speed
            pr_auc_macro=0.0,
            train_time_sec=round(self.train_time, 2),
            inference_latency_ms=round(latency, 6),
            zero_day_accuracy=round(zd_acc, 4),
            zero_day_f1=round(zd_f1, 4)
        )
        return res

    def save(self, path: Path):
        if PYG_AVAILABLE and self.model is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            torch.save(self.model.state_dict(), path)

    def load(self, path: Path):
        if PYG_AVAILABLE and self.model is not None:
            self.model.load_state_dict(torch.load(path, map_location="cpu"))
