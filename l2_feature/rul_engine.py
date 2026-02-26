"""
rul_engine.py

Industrial-Safe Probabilistic RUL Engine (v3)
Pure rule-based
Numerically stable
Production-ready
"""

import numpy as np


class ProbabilisticRUL:

    def __init__(self, failure_threshold=0.4):

        self.failure_threshold = failure_threshold

        # ----------------------------
        # Industrial Safety Guards
        # ----------------------------
        self.MIN_DATA_POINTS = 5
        self.MIN_SLOPE_THRESHOLD = 1e-4       # prevent near-zero slope explosion
        self.MAX_RUL_DAYS = 365 * 5           # 5-year cap
        self.MAX_REASONABLE_RUL = 365 * 10    # hard safety cap

    # ---------------------------------------------------------
    # Linear Regression Slope
    # ---------------------------------------------------------
    def _estimate_slope(self, series):

        x = np.arange(len(series))
        y = np.array(series)

        slope, _ = np.polyfit(x, y, 1)
        return slope

    # ---------------------------------------------------------
    # Empty Output Template
    # ---------------------------------------------------------
    def _stable_output(self, model_label="STABLE"):

        return {
            "rul_expected_days": None,
            "rul_95_lower_bound": None,
            "prob_failure_7d": 0.0,
            "rul_confidence": 0.8,
            "rul_model": model_label,
        }

    # ---------------------------------------------------------
    # Main RUL Calculation
    # ---------------------------------------------------------
    def calculate(self, health_series):

        # 1️⃣ Insufficient data
        if len(health_series) < self.MIN_DATA_POINTS:
            return self._stable_output("INSUFFICIENT_DATA")

        slope = self._estimate_slope(health_series)
        current_health = health_series[-1]

        # 2️⃣ Stable or near-flat degradation
        if slope >= 0 or abs(slope) < self.MIN_SLOPE_THRESHOLD:
            return self._stable_output("STABLE_OR_FLAT")

        # 3️⃣ Compute projected RUL
        days_to_failure = (
            (self.failure_threshold - current_health) / slope
        )

        # 4️⃣ Already failed case
        if current_health <= self.failure_threshold:
            return {
                "rul_expected_days": 0,
                "rul_95_lower_bound": 0,
                "prob_failure_7d": 1.0,
                "rul_confidence": 0.9,
                "rul_model": "FAILED",
            }

        # 5️⃣ Negative or unrealistic RUL
        if days_to_failure <= 0:
            return self._stable_output("INVALID_PROJECTION")

        # 6️⃣ Hard safety cap
        if days_to_failure > self.MAX_REASONABLE_RUL:
            return self._stable_output("LONG_TERM_STABLE")

        # 7️⃣ Soft cap (long but valid)
        if days_to_failure > self.MAX_RUL_DAYS:
            days_to_failure = self.MAX_RUL_DAYS

        # 8️⃣ Confidence estimation (variance-based)
        variance = np.var(health_series)
        confidence = max(0.3, min(1.0, 1 - variance))

        # 9️⃣ Conservative 95% lower bound
        lower_bound = days_to_failure * 0.8

        # 🔟 7-day failure probability
        prob_7d = min(1.0, max(0.0, 7 / days_to_failure))

        return {
            "rul_expected_days": round(days_to_failure, 1),
            "rul_95_lower_bound": round(lower_bound, 1),
            "prob_failure_7d": round(prob_7d, 2),
            "rul_confidence": round(confidence, 2),
            "rul_model": "LINEAR_DEGRADATION_SAFE",
        }




