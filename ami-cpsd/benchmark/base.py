"""
Base Class Definition for all AMI-CPSD v2.0 Benchmark Models.
Ensures standardized interface across classical, deep learning, graph, and anomaly models.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from benchmark.evaluator import BenchmarkResult


class BenchmarkModel(ABC):
    def __init__(self, name: str, track: str):
        self.name = name
        self.track = track
        self.model = None

    @abstractmethod
    def get_model(self):
        """Initializes and returns the underlying model instance."""
        pass

    @abstractmethod
    def train(self, *args, **kwargs) -> float:
        """Trains the model and returns elapsed training time in seconds."""
        pass

    @abstractmethod
    def predict(self, X):
        """Predicts class labels or anomaly flags."""
        pass

    @abstractmethod
    def evaluate(self, X_test, y_test, **kwargs) -> BenchmarkResult:
        """Evaluates the model on test data and returns a BenchmarkResult object."""
        pass

    @abstractmethod
    def save(self, path: Path):
        """Saves the trained model state to a file."""
        pass

    @abstractmethod
    def load(self, path: Path):
        """Loads a saved model state from a file."""
        pass
