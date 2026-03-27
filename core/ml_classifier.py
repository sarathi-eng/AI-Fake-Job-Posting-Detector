"""ML text classifier for fake job detection."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import joblib

from core.settings import settings


class MLTextClassifier:
    """Loads and runs a scikit-learn classifier for job description fraud probability."""

    def __init__(self):
        self.model = None
        self.available = False
        self._load_model()

    def _load_model(self) -> None:
        if not settings.model_enabled:
            return
        model_path = Path(settings.model_path)
        if not model_path.exists():
            return
        try:
            bundle = joblib.load(model_path)
            self.model = bundle["pipeline"] if isinstance(bundle, dict) and "pipeline" in bundle else bundle
            self.available = True
        except Exception:
            self.model = None
            self.available = False

    @staticmethod
    def _probability_to_confidence(probability: float) -> float:
        """
        Convert distance from 0.5 into confidence.
        - 0.5 means maximum uncertainty for binary classification.
        - Values closer to 0 or 1 imply stronger model certainty.
        - We clamp to [0.0, 0.99] so near-uncertain predictions stay low-confidence.
        """
        # Scale |p-0.5| from [0, 0.5] to [0, 1]; e.g., p=0.9 => 0.8 confidence signal.
        distance_from_center = abs(probability - 0.5) * 2
        return max(0.0, min(0.99, distance_from_center))

    def predict_fraud_probability(self, text: str) -> Optional[float]:
        if not self.available or self.model is None:
            return None
        try:
            probs = self.model.predict_proba([text])[0]
            if len(probs) >= 2:
                return float(probs[1])
            return float(probs[0])
        except Exception:
            return None

    def calculate_ml_score(self, text: str) -> Tuple[float, list[dict], bool]:
        """
        Returns (ml_risk, reasons, is_model_available).
        ml_risk is in 0..1.
        """
        prob = self.predict_fraud_probability(text)
        if prob is None:
            return 0.0, [], False

        reasons = [
            {
                "category": "ml_classifier",
                "signal": "ml_fraud_probability",
                "confidence": self._probability_to_confidence(prob),
                "message": f"ML classifier fraud probability: {prob * 100:.1f}%",
            }
        ]
        return max(0.0, min(1.0, prob)), reasons, True
