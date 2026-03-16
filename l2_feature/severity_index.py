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
        if vel_slope > self.cfg.get("vel_slope_alert", 0.01) * 2:
            return 85
        elif vel_slope > self.cfg.get("vel_slope_alert", 0.01):
            return 60
        elif vel_slope > 0:
            return 40
        return 10

    def _score_health(self, health):
        """
        health = payload['health_index'] di L1 logic (0-100)
        normalisasi ke 0..1
        """
        health_norm = max(0, min(health, 100)) / 100.0
        return int((1 - health_norm) * 100)

    # --------------------------------------------------------
    # Final Index
    # --------------------------------------------------------

    def calculate(self, payload, trend):
        """
        Main ISI calculation.
        """

        # pastikan health_index valid
        health_index = payload.get("health_index", 100)
        health_index = max(0, min(health_index, 100))
        payload["health_index"] = health_index

        iso_score = self._score_iso(payload.get("iso_zone", "ZONE_A"))
        crest_score = self._score_crest(payload.get("crest", 0))
        hf_score = self._score_hf_trend(trend.get("hf_slope", 0))
        vel_score = self._score_vel_trend(trend.get("vel_slope", 0))
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
