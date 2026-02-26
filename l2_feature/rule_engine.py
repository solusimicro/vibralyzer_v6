class RuleEngine:
    """
    Pure rule-based diagnostic engine.
    Tidak ada ML.
    """

    def __init__(self, class_config):
        self.cfg = class_config

    def evaluate(self, payload, trend):
        fault = "NORMAL"
        stage = "NONE"
        confidence = 0.0

        # Bearing Early
        if trend["hf_slope"] > 0.02 and trend["crest_slope"] > 0.01:
            fault = "BEARING"
            stage = "EARLY"
            confidence = 0.75

        # Developing
        if payload["crest"] > self.cfg["crest"]["developing"]:
            fault = "BEARING"
            stage = "DEVELOPING"
            confidence = 0.85

        return {
            "fault_type": fault,
            "fault_stage": stage,
            "confidence": confidence,
        }
