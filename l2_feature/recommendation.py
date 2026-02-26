"""
recommendation.py

Fungsi:
- Menghasilkan maintenance action berdasarkan:
    - final_status
    - fault_type
    - fault_stage
    - RUL
- Deterministic rule-based
- Explainable output
- ML-ready (future override possible)

Referensi:
- Industrial Maintenance Matrix
- L2 Final Status Tree
"""

from datetime import datetime


class RecommendationEngine:
    """
    Recommendation engine untuk L2.
    Tidak ada ML.
    Pure matrix-based deterministic.
    """

    def __init__(self, class_config):
        self.cfg = class_config

    def _base_matrix(self, final_status):
        """
        Mapping dasar berdasarkan final status.
        """
        matrix = {
            "NORMAL": ("CONTINUE_MONITORING", "LOW", 0),
            "OBSERVE": ("INCREASE_MONITORING", "LOW", 0),
            "EARLY_FAULT": ("INSPECT_WITHIN_14_DAYS", "MEDIUM", 14),
            "ALARM": ("PLAN_MAINTENANCE", "HIGH", 7),
            "CRITICAL": ("IMMEDIATE_SHUTDOWN", "URGENT", 0),
        }

        return matrix.get(final_status, ("MONITOR", "LOW", 0))

    def _fault_specific_adjustment(self, fault_type, fault_stage, base_action):
        """
        Adjust action berdasarkan tipe fault.
        """
        action, priority, days = base_action

        if fault_type == "BEARING":
            if fault_stage == "EARLY":
                return ("INSPECT_LUBRICATION", "MEDIUM", 14)
            if fault_stage == "DEVELOPING":
                return ("PLAN_BEARING_REPLACEMENT", "HIGH", 7)

        if fault_type == "UNBALANCE":
            return ("SCHEDULE_BALANCING", "MEDIUM", 7)

        if fault_type == "MISALIGNMENT":
            return ("CHECK_ALIGNMENT", "HIGH", 5)

        if fault_type == "LOOSENESS":
            return ("MECHANICAL_TIGHTENING_INSPECTION", "HIGH", 3)

        return action, priority, days

    def generate(
        self,
        asset_id,
        final_status,
        fault_type,
        fault_stage,
        estimated_rul_days,
    ):
        """
        Generate final recommendation payload.
        """

        base_action = self._base_matrix(final_status)

        action, priority, days = self._fault_specific_adjustment(
            fault_type,
            fault_stage,
            base_action,
        )

        # Override by RUL (safety rule)
        if estimated_rul_days is not None:
            if estimated_rul_days < 3:
                action = "IMMEDIATE_SHUTDOWN"
                priority = "URGENT"
                days = 0
            elif estimated_rul_days < 7:
                priority = "HIGH"

        return {
            "asset_id": asset_id,
            "action_code": action,
            "priority": priority,
            "recommended_within_days": days,
            "estimated_rul_days": estimated_rul_days,
            "timestamp": datetime.utcnow().isoformat(),
        }
