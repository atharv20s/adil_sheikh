"""
Transformer Encoder Deep Learning Model for Track 2.
"""

import math
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_pytorch
from benchmark.evaluator import evaluate_model


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1)]
        return x


class TransformerIDS(nn.Module):
    def __init__(self, input_size=52, d_model=128, nhead=8, num_layers=4, num_classes=13, dropout=0.2):
        super().__init__()
        self.proj = nn.Linear(input_size, d_model)
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

    def forward(self, x):
        x = self.proj(x)
        x = self.pos_encoder(x)
        out = self.transformer(x)
        out = torch.mean(out, dim=1) # Mean pooling over seq dimension
        return self.fc(out)


class TransformerBenchmark(BenchmarkModel):
    def __init__(self, input_size=52, num_classes=13):
        super().__init__(name="Transformer", track="deep_learning")
        self.input_size = input_size
        self.num_classes = num_classes
        self.model = self.get_model()

    def get_model(self):
        return TransformerIDS(input_size=self.input_size, num_classes=self.num_classes)

    def train(self, train_loader, val_loader, epochs=30, lr=0.0005, device="cpu"):
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
