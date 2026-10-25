"""
Physics-Informed Neural Network (PINN) Transformer for Track 6 (Physics-Aware).
Calculates and utilizes power flow constraints (P = VIcos(phi)) directly in inputs and loss.
"""

import math
import time
import logging
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.evaluator import evaluate_model
from benchmark.config import FEATURE_COLS
from benchmark.deep_learning.transformer import PositionalEncoding
from torch.utils.data import TensorDataset, DataLoader

logger = logging.getLogger(__name__)


class PINNTransformerNet(nn.Module):
    def __init__(self, input_size=52, d_model=128, nhead=8, num_layers=4, num_classes=13, dropout=0.2):
        super().__init__()
        # We append 1 physics residual feature to the input
        self.proj = nn.Linear(input_size + 1, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=256,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model, num_classes)

        # Retrieve index mapping from config
        self.voltage_idx = FEATURE_COLS.index("voltage")
        self.current_idx = FEATURE_COLS.index("current")
        self.active_power_idx = FEATURE_COLS.index("active_power")
        self.power_factor_idx = FEATURE_COLS.index("power_factor")

    def forward(self, x):
        # x: (batch, seq_len, input_size)
        v = x[:, :, self.voltage_idx]
        i = x[:, :, self.current_idx]
        pf = x[:, :, self.power_factor_idx]
        p_meas = x[:, :, self.active_power_idx]

        # Calculate V * I * cos(phi) / 1000
        p_calc = (v * i * pf) / 1000.0
        p_res = torch.abs(p_meas - p_calc).unsqueeze(-1) # (batch, seq_len, 1)

        # Concatenate residual as feature
        x_aug = torch.cat([x, p_res], dim=-1)

        x_proj = self.proj(x_aug)
        x_pos = self.pos_encoder(x_proj)
        out = self.transformer(x_pos)
        out = torch.mean(out, dim=1)
        logits = self.fc(out)
        return logits, p_res


class PhysicsAwareTransformerBenchmark(BenchmarkModel):
    def __init__(self, input_size=52, num_classes=13):
        super().__init__(name="Physics Transformer", track="physics_aware")
        self.input_size = input_size
        self.num_classes = num_classes
        self.model = self.get_model()

    def get_model(self):
        return PINNTransformerNet(input_size=self.input_size, num_classes=self.num_classes)

    def train(self, train_loader, val_loader, epochs=30, lr=0.0005, device="cpu", patience=5):
        logger.info(f"Training PINN Transformer on {device}...")
        self.model = self.model.to(device)
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        best_val_loss = float("inf")
        best_weights = None
        patience_counter = 0

        t0 = time.time()
        for epoch in range(1, epochs + 1):
            self.model.train()
            train_loss = 0.0
            for x_batch, y_batch in train_loader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                optimizer.zero_grad()
                logits, p_res = self.model(x_batch)
                
                # PINN Classification Loss + lambda * Physics Loss
                class_loss = criterion(logits, y_batch)
                physics_loss = torch.mean(p_res)
                
                # Attacking samples violation is captured via classification, 
                # and PINN regularization enforces physics-aware consistency.
                loss = class_loss + 0.1 * physics_loss
                
                loss.backward()
                optimizer.step()
                train_loss += loss.item() * x_batch.size(0)

            train_loss /= len(train_loader.dataset)

            # Validation
            self.model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for x_batch, y_batch in val_loader:
                    x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                    logits, p_res = self.model(x_batch)
                    loss = criterion(logits, y_batch) + 0.1 * torch.mean(p_res)
                    val_loss += loss.item() * x_batch.size(0)
            val_loss /= len(val_loader.dataset)

            logger.info(f"PINN Epoch {epoch}/{epochs} - Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

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
        logger.info(f"PINN training completed in {self.train_time:.2f} seconds.")
        return self.train_time

    def predict(self, loader, device="cpu"):
        self.model.eval()
        self.model.to(device)
        preds_list = []
        with torch.no_grad():
            for x_batch, _ in loader:
                x_batch = x_batch.to(device)
                logits, _ = self.model(x_batch)
                preds = torch.argmax(logits, dim=1)
                preds_list.append(preds.cpu().numpy())
        return np.concatenate(preds_list)

    def evaluate(self, test_loader, y_test, zero_day_data=None):
        return evaluate_model(
            model=self.model,
            X_test=test_loader,
            y_test=y_test,
            model_name=self.name,
            track=self.track,
            train_time=self.train_time,
            is_pytorch=True,
            sequence_input=True,
            zero_day_data=zero_day_data
        )

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.model.state_dict(), path)

    def load(self, path: Path):
        self.model.load_state_dict(torch.load(path, map_location="cpu"))
