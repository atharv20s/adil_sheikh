"""
Temporal Graph Transformer for Track 3 (Graph Neural Networks).
Combines Spatial Graph Attention (GAT) with a Temporal Transformer Encoder.
Executed conditionally if torch_geometric is installed.
"""

import logging
import numpy as np
from pathlib import Path
from benchmark.base import BenchmarkModel

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch_geometric.nn import GATConv
    PYG_AVAILABLE = True
except ImportError:
    PYG_AVAILABLE = False


if PYG_AVAILABLE:
    class TemporalGraphTransformerNet(nn.Module):
        def __init__(self, in_channels=52, hidden_dim=64, num_heads=4, num_classes=13):
            super().__init__()
            self.gat1 = GATConv(in_channels, hidden_dim, heads=num_heads, concat=True)
            self.gat2 = GATConv(hidden_dim * num_heads, hidden_dim, heads=1, concat=False)
            
            # Transformer for temporal dimension across sequence of graph states
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=hidden_dim,
                nhead=4,
                dim_feedforward=128,
                dropout=0.2,
                batch_first=True
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)
            self.classifier = nn.Linear(hidden_dim, num_classes)

        def forward(self, x_seq, edge_index):
            # x_seq shape: (batch_size, seq_len, num_nodes, in_channels)
            batch_size, seq_len, num_nodes, in_channels = x_seq.shape
            
            # Process spatial graph attention per sequence step
            seq_embeddings = []
            for t in range(seq_len):
                x_t = x_seq[:, t, :, :].reshape(-1, in_channels) # (batch_size * num_nodes, in_channels)
                h1 = torch.relu(self.gat1(x_t, edge_index))
                h2 = torch.relu(self.gat2(h1, edge_index))
                h2 = h2.reshape(batch_size, num_nodes, -1) # (batch_size, num_nodes, hidden_dim)
                seq_embeddings.append(h2.unsqueeze(1))
                
            # Concatenate along sequence dim: (batch_size, seq_len, num_nodes, hidden_dim)
            h_seq = torch.cat(seq_embeddings, dim=1)
            
            # Transpose to feed each node's time series to Transformer: (batch_size * num_nodes, seq_len, hidden_dim)
            h_seq = h_seq.transpose(1, 2).reshape(batch_size * num_nodes, seq_len, -1)
            
            h_trans = self.transformer(h_seq)
            h_final = torch.mean(h_trans, dim=1) # (batch_size * num_nodes, hidden_dim)
            
            logits = self.classifier(h_final)
            return logits


class TemporalGraphTransformerBenchmark(BenchmarkModel):
    def __init__(self, input_dim=52, num_classes=13):
        super().__init__(name="Temporal Graph Transformer", track="graph")
        self.input_dim = input_dim
        self.num_classes = num_classes
        if PYG_AVAILABLE:
            self.model = TemporalGraphTransformerNet(in_channels=input_dim, num_classes=num_classes)
        else:
            self.model = None

    def get_model(self):
        return self.model

    def train(self, snapshots, epochs=10, lr=0.001, device="cpu"):
        if not PYG_AVAILABLE:
            logger.warning("torch_geometric not installed. Skipping Temporal Graph Transformer training.")
            return 0.0
        # Placeholder for PyG training loop
        return 0.0

    def predict(self, snapshots):
        if not PYG_AVAILABLE:
            return np.array([])
        return np.array([])

    def evaluate(self, snapshots, y_test=None, zero_day_data=None):
        if not PYG_AVAILABLE:
            logger.warning("Skipping evaluation for Temporal Graph Transformer (PyG not available).")
            return {
                "model_name": self.name,
                "track": self.track,
                "accuracy": None,
                "weighted_f1": None,
                "status": "SKIPPED (PyG missing)"
            }
        return {}

    def save(self, path: Path):
        pass

    def load(self, path: Path):
        pass
