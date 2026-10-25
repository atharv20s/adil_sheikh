"""
Isolation Forest Anomaly Detection Model for Track 5 (Zero-Day Detection).
Trained ONLY on normal data (attack_type == 0).
"""

import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_classical
from benchmark.evaluator import evaluate_model


class IsolationForestBenchmark(BenchmarkModel):
    def __init__(self):
        super().__init__(name="Isolation Forest", track="anomaly")
        self.model = self.get_model()

    def get_model(self):
        return IsolationForest(
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )

    def train(self, X_normal_train):
        # We wrap it under classical train timer
        self.train_time = train_classical(self.model, X_normal_train, None)
        return self.train_time

    def predict(self, X):
        # IF predicts -1 for anomalies, 1 for normal
        preds = self.model.predict(X)
        return (preds == -1).astype(int)

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
        joblib.dump(self.model, path)

    def load(self, path: Path):
        self.model = joblib.load(path)
