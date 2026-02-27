import config


class L1Logic:

    def __init__(self):
        pass

    # ----------------------------
    # ISO Zone
    # ----------------------------
    def iso_zone(self, vel):

        if vel < config.VEL_WARNING:
            return "ZONE_A"
        elif vel < config.VEL_ALARM:
            return "ZONE_B"
        elif vel < 7.1:
            return "ZONE_C"
        else:
            return "ZONE_D"

    # ----------------------------
    # Health Index
    # ----------------------------
    def health_index(self, acc, crest, hf):

        score = 1.0

        if acc > config.ACC_RMS_ALARM:
            score -= 0.3

        if crest > config.CREST_LIMIT:
            score -= 0.3

        if hf > config.HF_LIMIT:
            score -= 0.3

        return max(score, 0)

    # ----------------------------
    # Evaluate
    # ----------------------------
    def evaluate(self, features):

        acc = features["acc_rms"]
        vel = features["vel_rms"]
        crest = features["crest"]
        hf = features["hf"]

        iso = self.iso_zone(vel)
        health = self.health_index(acc, crest, hf)

        state = "NORMAL"

        if iso in ("ZONE_C", "ZONE_D"):
            state = "ALARM"
        elif health < 0.7:
            state = "WARNING"

        # ✅ RETURN DICTIONARY (NOT TUPLE)
        return {
            "iso_zone": iso,
            "health_index": health,
            "state": state
        }


