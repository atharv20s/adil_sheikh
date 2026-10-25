"""
Data Loading and Preprocessing Module for AMI-CPSD v2.0.
Provides unified tabular, sequence, graph, and anomaly data loaders.
"""

import logging
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

import torch
from torch.utils.data import TensorDataset, DataLoader

# Import config
from benchmark.config import (
    DATASETS_DIR, FEATURE_COLS, LABEL_COL, BINARY_LABEL_COL, EXCLUDED_COLS, SEED
)

logger = logging.getLogger(__name__)


def load_tabular(train_rows=50000, val_rows=10000, test_rows=10000):
    """
    Loads tabular splits from CSV, applies imputation and scaling, and returns numpy arrays.
    """
    train_path = DATASETS_DIR / "train.csv"
    val_path = DATASETS_DIR / "validation.csv"
    test_path = DATASETS_DIR / "test.csv"

    if not all(p.exists() for p in [train_path, val_path, test_path]):
        raise FileNotFoundError("Missing train.csv, validation.csv, or test.csv in datasets/")

    logger.info(f"Loading tabular splits (train={train_rows}, val={val_rows}, test={test_rows})...")
    df_train = pd.read_csv(train_path, nrows=train_rows)
    df_val = pd.read_csv(val_path, nrows=val_rows)
    df_test = pd.read_csv(test_path, nrows=test_rows)

    X_train_raw = df_train[FEATURE_COLS]
    y_train = df_train[LABEL_COL].values
    X_val_raw = df_val[FEATURE_COLS]
    y_val = df_val[LABEL_COL].values
    X_test_raw = df_test[FEATURE_COLS]
    y_test = df_test[LABEL_COL].values

    # Impute & Scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    X_train = scaler.fit_transform(imputer.fit_transform(X_train_raw)).astype(np.float32)
    X_val = scaler.transform(imputer.transform(X_val_raw)).astype(np.float32)
    X_test = scaler.transform(imputer.transform(X_test_raw)).astype(np.float32)

    return X_train, y_train, X_val, y_val, X_test, y_test


def load_sequences(train_rows=50000, val_rows=10000, test_rows=10000, zero_day_rows=10000, seq_len=10, batch_size=256):
    """
    Loads data and builds sequential windows of shape (N, seq_len, num_features).
    Windows are built per-meter (i.e. temporal sequences do not cross meter boundaries).
    """
    train_path = DATASETS_DIR / "train.csv"
    val_path = DATASETS_DIR / "validation.csv"
    test_path = DATASETS_DIR / "test.csv"
    zd_path = DATASETS_DIR / "zero_day_test.csv"

    logger.info(f"Loading sequence splits (train={train_rows}, val={val_rows}, test={test_rows}, zero_day={zero_day_rows}, seq_len={seq_len})...")
    
    df_train = pd.read_csv(train_path, nrows=train_rows)
    df_val = pd.read_csv(val_path, nrows=val_rows)
    df_test = pd.read_csv(test_path, nrows=test_rows)
    df_zd = pd.read_csv(zd_path, nrows=zero_day_rows)

    # Imputer & Scaler fit on training feature columns
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    
    scaler.fit(imputer.fit_transform(df_train[FEATURE_COLS]))

    def build_group_sequences(df):
        # Sort by meter_id and timestamp to ensure temporal continuity
        df_sorted = df.sort_values(by=["meter_id", "timestamp"]).copy()
        
        # Scale features
        X_scaled = scaler.transform(imputer.transform(df_sorted[FEATURE_COLS])).astype(np.float32)
        y_vals = df_sorted[LABEL_COL].values
        meter_ids = df_sorted["meter_id"].values
        
        # Identify group boundaries
        change_idx = np.where(meter_ids[:-1] != meter_ids[1:])[0] + 1
        boundaries = [0] + list(change_idx) + [len(df_sorted)]
        
        X_seqs, y_seqs = [], []
        for i in range(len(boundaries) - 1):
            start = boundaries[i]
            end = boundaries[i+1]
            length = end - start
            if length >= seq_len:
                X_group = X_scaled[start:end]
                y_group = y_vals[start:end]
                # Extract sliding windows
                for j in range(length - seq_len + 1):
                    X_seqs.append(X_group[j : j + seq_len])
                    y_seqs.append(y_group[j + seq_len - 1]) # Target is the label of the last step
                    
        if len(X_seqs) == 0:
            return np.empty((0, seq_len, len(FEATURE_COLS)), dtype=np.float32), np.empty((0,), dtype=np.int64)
            
        return np.array(X_seqs, dtype=np.float32), np.array(y_seqs, dtype=np.int64)

    X_train_seq, y_train_seq = build_group_sequences(df_train)
    X_val_seq, y_val_seq = build_group_sequences(df_val)
    X_test_seq, y_test_seq = build_group_sequences(df_test)
    X_zd_seq, y_zd_seq = build_group_sequences(df_zd)
    
    y_zd_binary_seq = (y_zd_seq != 0).astype(int)

    # Convert to TensorDatasets & DataLoaders
    train_ds = TensorDataset(torch.tensor(X_train_seq), torch.tensor(y_train_seq))
    val_ds = TensorDataset(torch.tensor(X_val_seq), torch.tensor(y_val_seq))
    test_ds = TensorDataset(torch.tensor(X_test_seq), torch.tensor(y_test_seq))
    zd_ds = TensorDataset(torch.tensor(X_zd_seq), torch.tensor(y_zd_binary_seq))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    zd_loader = DataLoader(zd_ds, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader, y_test_seq, zd_loader, y_zd_binary_seq


def load_anomaly_data(train_rows=50000, val_rows=10000, test_rows=10000, zero_day_rows=10000):
    """
    Loads and prepares datasets for anomaly/zero-day detection.
    Training data consists ONLY of normal samples (attack_type == 0).
    Evaluation is done on binary labels (0 for normal, 1 for attack).
    """
    train_path = DATASETS_DIR / "train.csv"
    val_path = DATASETS_DIR / "validation.csv"
    test_path = DATASETS_DIR / "test.csv"
    zd_path = DATASETS_DIR / "zero_day_test.csv"

    logger.info("Loading anomaly splits (Normal only for training)...")
    
    # Train set: we load a larger chunk to extract enough Normal samples
    df_train_full = pd.read_csv(train_path, nrows=train_rows * 2)
    df_train_normal = df_train_full[df_train_full[BINARY_LABEL_COL] == 0].head(train_rows)
    
    df_val = pd.read_csv(val_path, nrows=val_rows)
    df_test = pd.read_csv(test_path, nrows=test_rows)
    df_zd = pd.read_csv(zd_path, nrows=zero_day_rows)

    # Impute & Scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    # Fit only on normal training data!
    X_train_normal = scaler.fit_transform(imputer.fit_transform(df_train_normal[FEATURE_COLS])).astype(np.float32)
    
    X_val = scaler.transform(imputer.transform(df_val[FEATURE_COLS])).astype(np.float32)
    y_val_binary = df_val[BINARY_LABEL_COL].values
    
    X_test = scaler.transform(imputer.transform(df_test[FEATURE_COLS])).astype(np.float32)
    y_test_binary = df_test[BINARY_LABEL_COL].values
    
    X_zd = scaler.transform(imputer.transform(df_zd[FEATURE_COLS])).astype(np.float32)
    y_zd_binary = df_zd[BINARY_LABEL_COL].values

    return X_train_normal, X_val, y_val_binary, X_test, y_test_binary, X_zd, y_zd_binary


def load_graph_data(num_snapshots=500):
    """
    Loads topology and states to build graph datasets.
    Since torch_geometric is optional, this checks importability.
    Each snapshot is a torch_geometric.data.Data object representing the grid state at a timestamp.
    """
    try:
        from torch_geometric.data import Data
    except ImportError:
        logger.warning("torch_geometric not found. GCN and GAT models will be skipped.")
        return None

    nodes_path = DATASETS_DIR / "nodes.csv"
    edges_path = DATASETS_DIR / "edges.csv"
    train_path = DATASETS_DIR / "train.csv"

    if not (nodes_path.exists() and edges_path.exists() and train_path.exists()):
        logger.warning("Graph topology files or train.csv missing. Skipping graph data load.")
        return None

    logger.info(f"Loading graph datasets ({num_snapshots} snapshots)...")
    
    # 1. Load topology
    df_nodes = pd.read_csv(nodes_path)
    df_edges = pd.read_csv(edges_path)
    
    # Node mapping: meter_id -> int index
    node_to_idx = {nid: idx for idx, nid in enumerate(df_nodes["node_id"])}
    
    # Build static edges
    edge_sources = df_edges["source_node"].map(node_to_idx).values
    edge_targets = df_edges["target_node"].map(node_to_idx).values
    
    # PyG expects edge_index of shape (2, num_edges)
    edge_index = torch.tensor(np.vstack([edge_sources, edge_targets]), dtype=torch.long)
    edge_attr = torch.tensor(df_edges["impedance_ohm"].values, dtype=torch.float32).unsqueeze(1)

    # 2. Load timestamps snapshots
    # To keep it efficient, we load the first chunks of train.csv, group by timestamp
    df_states = pd.read_csv(train_path, nrows=num_snapshots * len(node_to_idx))
    
    # Scale features
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()
    df_states_scaled = df_states.copy()
    df_states_scaled[FEATURE_COLS] = scaler.fit_transform(imputer.fit_transform(df_states[FEATURE_COLS]))
    
    # Group by timestamp
    snapshots = []
    grouped = df_states_scaled.groupby("timestamp")
    
    for t, group in grouped:
        if len(snapshots) >= num_snapshots:
            break
        # Create feature matrix x and target vector y of size (num_nodes, num_features/label)
        x = np.zeros((len(node_to_idx), len(FEATURE_COLS)), dtype=np.float32)
        y = np.zeros(len(node_to_idx), dtype=np.int64)
        
        # Populate values
        for _, row in group.iterrows():
            nid = row["meter_id"]
            if nid in node_to_idx:
                idx = node_to_idx[nid]
                x[idx] = row[FEATURE_COLS].values
                y[idx] = row[LABEL_COL]
                
        data = Data(
            x=torch.tensor(x, dtype=torch.float32),
            edge_index=edge_index,
            edge_attr=edge_attr,
            y=torch.tensor(y, dtype=torch.long)
        )
        snapshots.append(data)
        
    return snapshots


def load_multitask_data(train_rows=50000, val_rows=10000, test_rows=10000):
    """
    Loads tabular features and auxiliary multi-task targets.
    """
    train_path = DATASETS_DIR / "train.csv"
    val_path = DATASETS_DIR / "validation.csv"
    test_path = DATASETS_DIR / "test.csv"

    df_train = pd.read_csv(train_path, nrows=train_rows)
    df_val = pd.read_csv(val_path, nrows=val_rows)
    df_test = pd.read_csv(test_path, nrows=test_rows)

    X_train_raw = df_train[FEATURE_COLS]
    y_train_type = df_train[LABEL_COL].values
    
    X_val_raw = df_val[FEATURE_COLS]
    y_val_type = df_val[LABEL_COL].values
    
    X_test_raw = df_test[FEATURE_COLS]
    y_test_type = df_test[LABEL_COL].values

    # Impute & Scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    X_train = scaler.fit_transform(imputer.fit_transform(X_train_raw)).astype(np.float32)
    X_val = scaler.transform(imputer.transform(X_val_raw)).astype(np.float32)
    X_test = scaler.transform(imputer.transform(X_test_raw)).astype(np.float32)

    # Map auxiliary targets
    def extract_aux(df):
        sev = df["attack_severity"].fillna("Normal").map({"High": 3, "Medium": 2, "Low": 1}).fillna(0).values.astype(np.int64)
        stage = df["attack_stage"].fillna("Normal").map({"Recovery": 4, "Exploitation": 3, "Injection": 2, "Reconnaissance": 1, "Recon": 1}).fillna(0).values.astype(np.int64)
        consensus = df["failed_consensus"].fillna(0.0).values.astype(np.float32)
        recovery = df["recovery_time_sec"].fillna(0.0).values.astype(np.float32)
        return sev, stage, consensus, recovery

    train_sev, train_stage, train_cons, train_rec = extract_aux(df_train)
    val_sev, val_stage, val_cons, val_rec = extract_aux(df_val)
    test_sev, test_stage, test_cons, test_rec = extract_aux(df_test)

    # Pack targets into dictionaries
    y_train_mt = {
        "type": y_train_type,
        "severity": train_sev,
        "stage": train_stage,
        "consensus": train_cons,
        "recovery": train_rec
    }
    
    y_val_mt = {
        "type": y_val_type,
        "severity": val_sev,
        "stage": val_stage,
        "consensus": val_cons,
        "recovery": val_rec
    }
    
    y_test_mt = {
        "type": y_test_type,
        "severity": test_sev,
        "stage": test_stage,
        "consensus": test_cons,
        "recovery": test_rec
    }

    return X_train, y_train_mt, X_val, y_val_mt, X_test, y_test_mt
