class FinalStatus:
    """
    Menentukan state akhir berdasarkan ISO & health.
    """

    def __init__(self, class_cfg, failure_threshold):
        self.class_cfg = class_cfg
        self.failure_threshold = failure_threshold

    def determine(self, payload, rule_output):
        iso_zone = payload["iso_zone"]
        health = payload["health_index"]

        if iso_zone == "ZONE_D" or health < self.failure_threshold:
            return "CRITICAL"
        if iso_zone == "ZONE_C":
            return "ALARM"
        if rule_output["fault_stage"] == "EARLY":
            return "EARLY_FAULT"
        return "NORMAL"
