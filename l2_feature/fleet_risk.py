"""
fleet_risk.py

Fleet Risk Aggregation Engine
Pure rule-based
L2 → L3 bridge
"""

class FleetRiskEngine:

    def __init__(self):
        self.asset_risk = {}

    # ----------------------------------------
    # Risk per Asset
    # ----------------------------------------
    def calculate_asset_risk(
        self,
        asset_id,
        severity_score,
        prob_failure_7d,
        final_status,
    ):

        status_weight = {
            "NORMAL": 0,
            "WATCH": 20,
            "ALARM": 50,
            "CRITICAL": 80,
        }.get(final_status, 0)

        risk_score = (
            0.5 * severity_score
            + 0.3 * (prob_failure_7d * 100)
            + 0.2 * status_weight
        )

        risk_score = min(100, round(risk_score, 2))

        self.asset_risk[asset_id] = risk_score

        return {
            "asset_risk_score": risk_score,
            "asset_risk_level": self._risk_label(risk_score),
        }

    # ----------------------------------------
    # Fleet Level Aggregation
    # ----------------------------------------
    def calculate_fleet_risk(self):

        if not self.asset_risk:
            return None

        avg_risk = sum(self.asset_risk.values()) / len(self.asset_risk)

        return {
            "fleet_risk_score": round(avg_risk, 2),
            "fleet_risk_level": self._risk_label(avg_risk),
            "assets_monitored": len(self.asset_risk),
        }

    # ----------------------------------------
    # Risk Label
    # ----------------------------------------
    def _risk_label(self, score):

        if score < 25:
            return "LOW"
        elif score < 50:
            return "MODERATE"
        elif score < 75:
            return "HIGH"
        else:
            return "CRITICAL"
