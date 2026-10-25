"""
Multi-Task Intrusion Detection System (IDS) for Track 7.
Predicts attack type, severity, stage, consensus failures, and recovery times simultaneously.
"""

import time
import logging
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.evaluator import evaluate_model
from torch.utils.data import TensorDataset, DataLoader

logger = logging.getLogger(__name__)


class MultiTaskIDSNet(nn.Module):
    def __init__(self, input_dim=52):
        super().__init__()
        # Shared Encoder representation
        self.shared_encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        # Task Heads
        self.type_head = nn.Linear(128, 13)       # 13 attack types
        self.severity_head = nn.Linear(128, 4)   # 4 severity classes
        self.stage_head = nn.Linear(128, 5)      # 5 stages
        self.consensus_head = nn.Linear(128, 1)  # consensus failure (binary logits)
        self.recovery_head = nn.Linear(128, 1)   # recovery time (regression logits)

    def forward(self, x):
        feat = self.shared_encoder(x)
        type_logits = self.type_head(feat)
        severity_logits = self.severity_head(feat)
        stage_logits = self.stage_head(feat)
        consensus_logits = self.consensus_head(feat)
        recovery_logits = self.recovery_head(feat)
        return type_logits, severity_logits, stage_logits, consensus_logits, recovery_logits


class MultiTaskIDSBenchmark(BenchmarkModel):
    def __init__(self, input_dim=52):
        super().__init__(name="Multi-Task IDS", track="multi_task")
        self.input_dim = input_dim
        self.model = self.get_model()

    def get_model(self):
        return MultiTaskIDSNet(input_dim=self.input_dim)

    def train(self, X_train, y_train_mt, X_val, y_val_mt, epochs=30, lr=0.001, batch_size=512, device="cpu", patience=5):
        logger.info(f"Training Multi-Task model on {device}...")
        self.model = self.model.to(device)
        optimizer = optim.Adam(self.model.parameters(), lr=lr)

        # Loss functions
        criterion_ce = nn.CrossEntropyLoss()
        criterion_bce = nn.BCEWithLogitsLoss()
        criterion_mse = nn.MSELoss()

        # Pack tensors
        train_ds = TensorDataset(
            torch.tensor(X_train, dtype=torch.float32),
            torch.tensor(y_train_mt["type"], dtype=torch.long),
            torch.tensor(y_train_mt["severity"], dtype=torch.long),
            torch.tensor(y_train_mt["stage"], dtype=torch.long),
            torch.tensor(y_train_mt["consensus"], dtype=torch.float32),
            torch.tensor(y_train_mt["recovery"], dtype=torch.float32)
        )
        val_ds = TensorDataset(
            torch.tensor(X_val, dtype=torch.float32),
            torch.tensor(y_val_mt["type"], dtype=torch.long),
            torch.tensor(y_val_mt["severity"], dtype=torch.long),
            torch.tensor(y_val_mt["stage"], dtype=torch.long),
            torch.tensor(y_val_mt["consensus"], dtype=torch.float32),
            torch.tensor(y_val_mt["recovery"], dtype=torch.float32)
        )

        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

        best_val_loss = float("inf")
        best_weights = None
        patience_counter = 0

        t0 = time.time()
        for epoch in range(1, epochs + 1):
            self.model.train()
            train_loss = 0.0
            for x_b, y_t_b, y_s_b, y_st_b, y_c_b, y_r_b in train_loader:
                x_b = x_b.to(device)
                y_t_b, y_s_b, y_st_b = y_t_b.to(device), y_s_b.to(device), y_st_b.to(device)
                y_c_b, y_r_b = y_c_b.to(device), y_r_b.to(device)

                optimizer.zero_grad()
                type_l, sev_l, stage_l, cons_l, rec_l = self.model(x_b)

                # Losses
                loss_type = criterion_ce(type_l, y_t_b)
                loss_sev = criterion_ce(sev_l, y_s_b)
                loss_stage = criterion_ce(stage_l, y_st_b)
                loss_cons = criterion_bce(cons_l.squeeze(-1), y_c_b)
                loss_rec = criterion_mse(rec_l.squeeze(-1), y_r_b)

                # Combined Loss
                loss = loss_type + loss_sev + loss_stage + loss_cons + 0.01 * loss_rec

                loss.backward()
                optimizer.step()
                train_loss += loss.item() * x_b.size(0)

            train_loss /= len(train_loader.dataset)

            # Validation
            self.model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for x_b, y_t_b, y_s_b, y_st_b, y_c_b, y_r_b in val_loader:
                    x_b = x_b.to(device)
                    y_t_b, y_s_b, y_st_b = y_t_b.to(device), y_s_b.to(device), y_st_b.to(device)
                    y_c_b, y_r_b = y_c_b.to(device), y_r_b.to(device)

                    type_l, sev_l, stage_l, cons_l, rec_l = self.model(x_b)
                    loss = (
                        criterion_ce(type_l, y_t_b) +
                        criterion_ce(sev_l, y_s_b) +
                        criterion_ce(stage_l, y_st_b) +
                        criterion_bce(cons_l.squeeze(-1), y_c_b) +
                        0.01 * criterion_mse(rec_l.squeeze(-1), y_r_b)
                    )
                    val_loss += loss.item() * x_b.size(0)
            val_loss /= len(val_loader.dataset)

            logger.info(f"Multi-Task Epoch {epoch}/{epochs} - Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_weights = self.model.state_dict()
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    logger.info(f"Early stopping triggered at epoch {epoch}")
                    break

        if best_weights is not None:
            self.model.load_state_dict(best_weights)

        self.train_time = time.time() - t0
        logger.info(f"Multi-Task training completed in {self.train_time:.2f} seconds.")
        return self.train_time

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            type_logits, _, _, _, _ = self.model(x_tensor)
            return torch.argmax(type_logits, dim=1).numpy()

    def predict_proba(self, X):
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            type_logits, _, _, _, _ = self.model(x_tensor)
            return torch.softmax(type_logits, dim=1).numpy()

    def evaluate(self, X_test, y_test, zero_day_data=None):
        # We evaluate on primary attack type task
        probs = self.predict_proba(X_test)
        return evaluate_model(
            model=self.model,
            X_test=X_test,
            y_test=y_test,
            model_name=self.name,
            track=self.track,
            train_time=self.train_time,
            is_pytorch=True,
            zero_day_data=zero_day_data
        )

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.model.state_dict(), path)

    def load(self, path: Path):
        self.model.load_state_dict(torch.load(path, map_location="cpu"))
