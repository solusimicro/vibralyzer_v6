"""
severity_index.py

Industrial Severity Index (ISI)

Menghasilkan skor 0–100
Digunakan untuk:
- Ranking asset
- Maintenance priority
- Enterprise dashboard

Pure rule-based weighted scoring.
ML-ready (weights bisa di-tune).
"""

class SeverityIndex:
    """
    Industrial Severity Index calculator.
    """

    def __init__(self, class_config):
        self.cfg = class_config

        # Default weights (configurable)
        self.weights = {
            "iso": 0.35,
            "crest": 0.20,
            "hf_trend": 0.15,
            "vel_trend": 0.15,
            "health": 0.15,
        }

    # --------------------------------------------------------
    # Individual Scoring Blocks
    # --------------------------------------------------------

    def _score_iso(self, iso_zone):
        mapping = {
            "ZONE_A": 10,
            "ZONE_B": 40,
            "ZONE_C": 70,
            "ZONE_D": 95,
        }
        return mapping.get(iso_zone, 0)

    def _score_crest(self, crest):
        if crest > self.cfg["crest"]["critical"]:
            return 100
        elif crest > self.cfg["crest"]["developing"]:
            return 75
        elif crest > self.cfg["crest"]["early"]:
            return 50
        return 10

    def _score_hf_trend(self, hf_slope):
        if hf_slope > 0.05:
            return 90
        elif hf_slope > 0.02:
            return 60
        elif hf_slope > 0:
            return 40
        return 10

    def _score_vel_trend(self, vel_slope):
        if vel_slope > self.cfg["vel_slope_alert"] * 2:
            return 85
        elif vel_slope > self.cfg["vel_slope_alert"]:
            return 60
        elif vel_slope > 0:
            return 40
        return 10

    def _score_health(self, health):
        # health 1.0 = perfect
        return int((1 - health) * 100)

    # --------------------------------------------------------
    # Final Index
    # --------------------------------------------------------

    def calculate(self, payload, trend):
        """
        Main ISI calculation.
        """

        iso_score = self._score_iso(payload["iso_zone"])
        crest_score = self._score_crest(payload["crest"])
        hf_score = self._score_hf_trend(trend["hf_slope"])
        vel_score = self._score_vel_trend(trend["vel_slope"])
        health_score = self._score_health(payload["health_index"])

        isi = (
            iso_score * self.weights["iso"]
            + crest_score * self.weights["crest"]
            + hf_score * self.weights["hf_trend"]
            + vel_score * self.weights["vel_trend"]
            + health_score * self.weights["health"]
        )

        return {
            "industrial_severity_index": round(isi, 2),
            "component_scores": {
                "iso": iso_score,
                "crest": crest_score,
                "hf_trend": hf_score,
                "vel_trend": vel_score,
                "health": health_score,
            },
        }
