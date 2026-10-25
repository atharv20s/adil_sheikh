"""
Autoencoder Anomaly Detection Model for Track 5 (Zero-Day Detection).
Trained ONLY on normal data (attack_type == 0).
"""

import torch
import torch.nn as nn
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_anomaly_ae
from benchmark.evaluator import evaluate_model


class AutoencoderNet(nn.Module):
    def __init__(self, input_dim=52):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_dim)
        )

    def forward(self, x):
        latent = self.encoder(x)
        recon = self.decoder(latent)
        return recon


class AutoencoderBenchmark(BenchmarkModel):
    def __init__(self, input_dim=52):
        super().__init__(name="Autoencoder", track="anomaly")
        self.input_dim = input_dim
        self.model = self.get_model()
        self.threshold = 0.0

    def get_model(self):
        return AutoencoderNet(input_dim=self.input_dim)

    def train(self, X_normal_train, X_val, y_val_binary, epochs=30, batch_size=256, lr=0.001, device="cpu"):
        self.train_time = train_anomaly_ae(
            model=self.model,
            X_normal=X_normal_train,
            val_data=(X_val, y_val_binary),
            epochs=epochs,
            batch_size=batch_size,
            lr=lr,
            device=device
        )
        # Store threshold on class level
        self.threshold = self.model.threshold
        return self.train_time

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            recon = self.model(x_tensor)
            mse = torch.mean((x_tensor - recon) ** 2, dim=1).cpu().numpy()
            return (mse > self.threshold).astype(int)

    def evaluate(self, X_test, y_test_binary, zero_day_data=None):
        return evaluate_model(
            model=self.model,
            X_test=X_test,
            y_test=y_test_binary,
            model_name=self.name,
            track=self.track,
            train_time=self.train_time,
            is_anomaly=True,
            zero_day_data=zero_day_data
        )

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Save both state_dict and threshold
        state = {
            "state_dict": self.model.state_dict(),
            "threshold": self.threshold
        }
        torch.save(state, path)

    def load(self, path: Path):
        state = torch.load(path, map_location="cpu")
        self.model.load_state_dict(state["state_dict"])
        self.threshold = state["threshold"]
        self.model.threshold = self.threshold
