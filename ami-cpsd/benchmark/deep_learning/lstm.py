"""
LSTM Deep Learning Model for Track 2 (Sequence Classification).
"""

import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_pytorch
from benchmark.evaluator import evaluate_model


class LSTMNet(nn.Module):
    def __init__(self, input_size=52, hidden_size=128, num_layers=2, num_classes=13):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # x shape: (batch, seq_len, input_size)
        out, _ = self.lstm(x)
        # Take the output of the last time step
        out = out[:, -1, :]
        return self.fc(out)


class LSTMBenchmark(BenchmarkModel):
    def __init__(self, input_size=52, num_classes=13):
        super().__init__(name="LSTM", track="deep_learning")
        self.input_size = input_size
        self.num_classes = num_classes
        self.model = self.get_model()

    def get_model(self):
        return LSTMNet(input_size=self.input_size, num_classes=self.num_classes)

    def train(self, train_loader, val_loader, epochs=30, lr=0.001, device="cpu"):
        self.train_time = train_pytorch(
            model=self.model,
            train_loader=train_loader,
            val_loader=val_loader,
            epochs=epochs,
            lr=lr,
            patience=5,
            device=device
        )
        return self.train_time

    def predict(self, loader, device="cpu"):
        self.model.eval()
        self.model.to(device)
        preds_list = []
        with torch.no_grad():
            for x_batch, _ in loader:
                x_batch = x_batch.to(device)
                outputs = self.model(x_batch)
                preds = torch.argmax(outputs, dim=1)
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
