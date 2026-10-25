"""
Multi-Layer Perceptron (MLP) Deep Learning Model for Track 2.
"""

import torch
import torch.nn as nn
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_pytorch
from benchmark.evaluator import evaluate_model
from torch.utils.data import DataLoader, TensorDataset


class MLPNet(nn.Module):
    def __init__(self, input_dim=52, num_classes=13):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.net(x)


class MLPBenchmark(BenchmarkModel):
    def __init__(self, input_dim=52, num_classes=13):
        super().__init__(name="MLP", track="deep_learning")
        self.input_dim = input_dim
        self.num_classes = num_classes
        self.model = self.get_model()

    def get_model(self):
        return MLPNet(input_dim=self.input_dim, num_classes=self.num_classes)

    def train(self, X_train, y_train, X_val, y_val, epochs=30, lr=0.001, batch_size=512, device="cpu"):
        train_ds = TensorDataset(torch.tensor(X_train), torch.tensor(y_train, dtype=torch.long))
        val_ds = TensorDataset(torch.tensor(X_val), torch.tensor(y_val, dtype=torch.long))
        
        train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
        
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

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            outputs = self.model(x_tensor)
            return torch.argmax(outputs, dim=1).numpy()

    def predict_proba(self, X):
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.tensor(X, dtype=torch.float32)
            outputs = self.model(x_tensor)
            return torch.softmax(outputs, dim=1).numpy()

    def evaluate(self, X_test, y_test, zero_day_data=None):
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
