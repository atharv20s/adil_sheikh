"""
Linear SVM Benchmark Model for Track 1 (Classical ML).
Uses LinearSVC wrapped in CalibratedClassifierCV to enable probability predictions.
"""

import joblib
from pathlib import Path
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_classical
from benchmark.evaluator import evaluate_model


class SVMBenchmark(BenchmarkModel):
    def __init__(self):
        super().__init__(name="SVM", track="classical")
        self.model = self.get_model()

    def get_model(self):
        base_svc = LinearSVC(
            max_iter=2000,
            random_state=42,
            dual="auto"
        )
        return CalibratedClassifierCV(base_svc, cv=3, n_jobs=-1)

    def train(self, X_train, y_train):
        self.train_time = train_classical(self.model, X_train, y_train)
        return self.train_time

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def evaluate(self, X_test, y_test, zero_day_data=None):
        probs = self.predict_proba(X_test)
        return evaluate_model(
            model=self.model,
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
        joblib.dump(self.model, path)

    def load(self, path: Path):
        self.model = joblib.load(path)
