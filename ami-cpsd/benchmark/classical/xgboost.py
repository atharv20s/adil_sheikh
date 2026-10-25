"""
XGBoost Benchmark Model for Track 1 (Classical ML).
Uses a wrapper to handle target class label mapping for non-contiguous labels.
"""

import joblib
from pathlib import Path
import numpy as np
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_classical
from benchmark.evaluator import evaluate_model


class XGBoostWrapper:
    """Wraps XGBoost model to handle inverse mapping of class labels."""
    def __init__(self, model, label_encoder):
        self.model = model
        self.label_encoder = label_encoder
        self.classes_ = label_encoder.classes_

    def predict(self, X):
        preds = self.model.predict(X)
        return self.label_encoder.inverse_transform(preds)

    def predict_proba(self, X):
        return self.model.predict_proba(X)


class XGBoostBenchmark(BenchmarkModel):
    def __init__(self):
        super().__init__(name="XGBoost", track="classical")
        self.model = self.get_model()
        self.label_encoder = LabelEncoder()

    def get_model(self):
        return XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )

    def train(self, X_train, y_train):
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        self.train_time = train_classical(self.model, X_train, y_train_encoded)
        return self.train_time

    def predict(self, X):
        preds_encoded = self.model.predict(X)
        return self.label_encoder.inverse_transform(preds_encoded)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def evaluate(self, X_test, y_test, zero_day_data=None):
        wrapper = XGBoostWrapper(self.model, self.label_encoder)
        probs = self.predict_proba(X_test)
        return evaluate_model(
            model=wrapper,
            X_test=X_test,
            y_test=y_test,
            model_name=self.name,
            track=self.track,
            train_time=self.train_time,
            y_test_probs=probs,
            zero_day_data=zero_day_data
        )

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Save both model and label encoder
        state = {
            "model": self.model,
            "label_encoder": self.label_encoder
        }
        joblib.dump(state, path)

    def load(self, path: Path):
        state = joblib.load(path)
        self.model = state["model"]
        self.label_encoder = state["label_encoder"]
