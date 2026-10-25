"""
Random Forest Benchmark Model for Track 1 (Classical ML).
"""

import json
import joblib
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from benchmark.base import BenchmarkModel
from benchmark.trainer import train_classical
from benchmark.evaluator import evaluate_model
from benchmark.config import RESULTS_DIR


class RandomForestBenchmark(BenchmarkModel):
    def __init__(self):
        super().__init__(name="Random Forest", track="classical")
        self.model = self.get_model()

    def get_model(self):
        return RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )

    def train(self, X_train, y_train, feature_names=None):
        self.train_time = train_classical(self.model, X_train, y_train)
        if feature_names is not None:
            self.export_feature_importance(feature_names)
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

    def export_feature_importance(self, feature_names):
        """Exports RF feature importance rankings to results/reports/."""
        importances = self.model.feature_importances_
        df_imp = pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False)
        
        out_path = RESULTS_DIR / "reports" / "random_forest_feature_importance.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Convert to dict for json serialization
        df_imp.set_index("feature")["importance"].to_json(out_path, indent=4)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)

    def load(self, path: Path):
        self.model = joblib.load(path)
