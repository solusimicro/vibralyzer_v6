"""
interpretation.py

Fungsi:
- Mengubah hasil RuleEngine + TrendEngine menjadi
  interpretasi teknis yang explainable.
- Menghitung severity_score (legacy scoring)
- Menghitung Industrial Severity Index (ISI)
- Validasi konsistensi pola fault (pattern validation)
- Menentukan dominant indicator (physics driver)

Pure rule-based.
ML-ready.
"""

from datetime import datetime
from severity_index import SeverityIndex


class InterpretationEngine:
    """
    Engineering-grade interpretation engine (L2).
    Pure technical diagnostic.
    """

    def __init__(self, class_config):
        self.cfg = class_config
        self.severity_engine = SeverityIndex(class_config)

    # =========================================================
    # LEGACY SEVERITY SCORE (Backward Compatibility)
    # =========================================================

    def _severity_score(self, payload, trend, fault_stage):

        score = 0

        iso_zone = payload.get("iso_zone", "ZONE_A")
        iso_weight = {
            "ZONE_A": 10,
            "ZONE_B": 30,
            "ZONE_C": 60,
            "ZONE_D": 90,
        }
        score += iso_weight.get(iso_zone, 0)

        crest = payload.get("crest", 0)

        crest_crit = self.cfg.get("crest", {}).get("critical", 4.0)
        crest_dev = self.cfg.get("crest", {}).get("developing", 2.5)
        crest_early = self.cfg.get("crest", {}).get("early", 1.8)
        
        if crest > crest_crit:
          score += 30
        elif crest > crest_dev:
            score += 20
        elif crest > crest_early:
            score += 10

        if trend.get("vel_slope", 0) > self.cfg["vel_slope_alert"]:
            score += 10

        stage_multiplier = {
            "NONE": 0,
            "EARLY": 5,
            "DEVELOPING": 15,
            "CRITICAL": 30,
        }

        score += stage_multiplier.get(fault_stage, 0)

        return min(score, 100)

    # =========================================================
    # PATTERN VALIDATION (Physics Consistency Check)
    # =========================================================

    def _validate_fault_pattern(self, payload, trend, fault_type):

      score = 0

      vel = payload.get("vel_rms", 0)
      crest = payload.get("crest", 0)
      hf = payload.get("hf", 0)

      vel_warn = self.cfg.get("velocity", {}).get("warning", 4.5)
      crest_early = self.cfg.get("crest", {}).get("early", 1.8)
      crest_dev = self.cfg.get("crest", {}).get("developing", 2.5)
      hf_alert = self.cfg.get("hf", {}).get("alert", 0.2)

      min_hf_slope = self.cfg.get("min_hf_slope_explain", 0.001)
      min_vel_slope = self.cfg.get("min_vel_slope_explain", 0.001)

      # Bearing pattern validation
      if fault_type == "BEARING":

          if hf > hf_alert:
              score += 1

          if crest > crest_dev:
              score += 1

          if trend.get("hf_slope", 0) > min_hf_slope:
              score += 1

      # Unbalance pattern validation
      elif fault_type == "UNBALANCE":

          if vel > vel_warn:
              score += 1

          if trend.get("vel_slope", 0) > min_vel_slope:
              score += 1

      # Misalignment pattern validation
      elif fault_type == "MISALIGNMENT":

          if crest > crest_early:
              score += 1

          if vel > vel_warn:
              score += 1

      # Looseness pattern validation
      elif fault_type == "LOOSENESS":

          if vel > vel_warn:
              score += 1

          if crest > crest_early:
              score += 1

      return score


    # =========================================================
    # DOMINANT INDICATOR (Physics Driver)
    # =========================================================

    def _dominant_indicator(self, payload):

        contributions = {
            "velocity": payload.get("vel_rms", 0),
            "crest": payload.get("crest", 0),
            "hf": payload.get("hf", 0),
        }

        return max(contributions, key=contributions.get)

    # =========================================================
    # ROOT EXPLANATION BUILDER
    # =========================================================
    def _build_root_indicators(self, payload, trend, fault_type):

        indicators = []

        vel_slope = trend.get("vel_slope", 0)
        hf_slope = trend.get("hf_slope", 0)

        min_vel_slope = self.cfg.get("min_vel_slope_explain", 0.001)
        min_hf_slope = self.cfg.get("min_hf_slope_explain", 0.001)

        # Trend explanation with threshold filtering
        if vel_slope > min_vel_slope:
            indicators.append(
                f"Velocity increasing trend ({vel_slope:.3f} mm/s per window)"
            )

        if hf_slope > min_hf_slope:
            indicators.append(
                f"HF RMS increasing ({hf_slope:.3f} per window)"
            )

        crest = payload.get("crest", 0)
        if crest > self.cfg["crest"]["early"]:
            indicators.append(
                f"Crest factor elevated ({crest:.2f})"
            )

        health = payload.get("health_index", 1.0)
        if health < 0.7:
            indicators.append(
                f"Health index degraded ({health:.2f})"
            )

        # Fault-specific explanation
        if fault_type == "BEARING":
            indicators.append(
                "High-frequency vibration signature typical of bearing defect"
            )

        elif fault_type == "UNBALANCE":
            indicators.append(
                "Dominant 1X rotational vibration characteristic"
            )

        elif fault_type == "MISALIGNMENT":
            indicators.append(
                "Elevated 2X harmonic vibration signature"
            )

        elif fault_type == "LOOSENESS":
            indicators.append(
                "Broadband vibration energy increase"
            )

        return indicators
   
    # =========================================================
    # MAIN INTERPRETATION
    # =========================================================

    def interpret(self, payload, trend, rule_output):

        fault_type = rule_output.get("fault_type", "NORMAL")
        fault_stage = rule_output.get("fault_stage", "NONE")
        base_confidence = rule_output.get("confidence", 0.0)
        
        # ✅ Validasi health_index
        payload["health_index"] = max(0.0, min(payload.get("health_index", 1.0), 1.0))
        
        # 1️⃣ Legacy severity
        severity_score = self._severity_score(
            payload,
            trend,
            fault_stage
        )

        # 2️⃣ Industrial Severity Index (Enterprise KPI)
        isi_output = self.severity_engine.calculate(
            payload,
            trend
        )

        # 3️⃣ Root technical explanation
        root_indicators = self._build_root_indicators(
            payload,
            trend,
            fault_type
        )

        # 4️⃣ Physics pattern validation
        pattern_score = self._validate_fault_pattern(
            payload,
            trend,
            fault_type
        )

        # 5️⃣ Dominant physical driver
        dominant_indicator = self._dominant_indicator(payload)

        # 6️⃣ Confidence refinement
        indicator_boost = min(len(root_indicators) * 0.05, 0.2)
        pattern_boost = min(pattern_score * 0.05, 0.15)

        final_confidence = min(
            base_confidence + indicator_boost + pattern_boost,
            1.0
        )

        # 7️⃣ Final structured output
        return {
            "fault_type": fault_type,
            "fault_stage": fault_stage,
            "confidence": round(final_confidence, 2),

            # Legacy scoring
            "severity_score": severity_score,

            # Industrial KPI
            **isi_output,

            # Technical enrichment
            "dominant_indicator": dominant_indicator,
            "pattern_validation_score": pattern_score,

            "root_indicators": root_indicators,
            "interpreted_at": datetime.utcnow().isoformat(),
        }
