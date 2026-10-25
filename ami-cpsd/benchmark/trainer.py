"""
Training Execution Module for AMI-CPSD v2.0.
Contains unified fit loops for Classical, Deep Learning, and Anomaly Detection models.
"""

import logging
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

logger = logging.getLogger(__name__)


def train_classical(model, X_train, y_train):
    """Trains a scikit-learn or similar classical classifier and returns elapsed time."""
    logger.info(f"Training classical model {model.__class__.__name__}...")
    t0 = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - t0
    logger.info(f"Training completed in {elapsed:.2f} seconds.")
    return elapsed


def train_pytorch(model, train_loader, val_loader, epochs=30, lr=1e-3, patience=5, device="cpu"):
    """
    Standard PyTorch training loop with Adam, CrossEntropyLoss, and early stopping.
    """
    logger.info(f"Training PyTorch model {model.__class__.__name__} on {device}...")
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    best_val_loss = float("inf")
    best_weights = None
    patience_counter = 0

    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * x_batch.size(0)

        train_loss /= len(train_loader.dataset)

        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x_batch, y_batch in val_loader:
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                outputs = model(x_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item() * x_batch.size(0)
        val_loss /= len(val_loader.dataset)

        logger.info(f"Epoch {epoch}/{epochs} - Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

        # Early stopping check
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = model.state_dict()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                logger.info(f"Early stopping triggered at epoch {epoch}")
                break

    # Restore best weights
    if best_weights is not None:
        model.load_state_dict(best_weights)

    elapsed = time.time() - t0
    logger.info(f"PyTorch training completed in {elapsed:.2f} seconds.")
    return elapsed


def train_anomaly_ae(model, X_normal, val_data, epochs=30, batch_size=256, lr=1e-3, device="cpu"):
    """
    Trains an Autoencoder on normal samples only, using MSE loss.
    Tuned reconstruction threshold is selected using validation data to maximize F1 score.
    """
    logger.info("Training Autoencoder on normal data...")
    model = model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    # Create PyTorch datasets
    tensor_x = torch.tensor(X_normal, dtype=torch.float32)
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(tensor_x, tensor_x), batch_size=batch_size, shuffle=True
    )

    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        epoch_loss = 0.0
        for x_batch, _ in loader:
            x_batch = x_batch.to(device)
            optimizer.zero_grad()
            recon = model(x_batch)
            loss = criterion(recon, x_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * x_batch.size(0)
        epoch_loss /= len(loader.dataset)
        if epoch % 5 == 0 or epoch == 1:
            logger.info(f"AE Epoch {epoch}/{epochs} - Reconstruction Loss: {epoch_loss:.6f}")

    elapsed = time.time() - t0
    logger.info(f"Autoencoder training finished in {elapsed:.2f} seconds.")

    # Select reconstruction threshold on validation set
    X_val, y_val_binary = val_data
    model.eval()
    with torch.no_grad():
        val_tensor = torch.tensor(X_val, dtype=torch.float32).to(device)
        val_recon = model(val_tensor)
        val_errors = torch.mean((val_tensor - val_recon) ** 2, dim=1).cpu().numpy()

    # Grid search for reconstruction error threshold to maximize validation F1 score
    best_threshold = 0.0
    best_f1 = 0.0
    percentiles = np.percentile(val_errors, np.linspace(80, 99.9, 100))
    from sklearn.metrics import f1_score
    for threshold in percentiles:
        preds = (val_errors > threshold).astype(int)
        f1 = f1_score(y_val_binary, preds, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    logger.info(f"AE Threshold chosen: {best_threshold:.6f} (Validation F1: {best_f1:.4f})")
    model.threshold = best_threshold
    return elapsed
