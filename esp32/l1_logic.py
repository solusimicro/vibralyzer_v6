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
        score = 100

        # ACC RMS
        if acc > config.ACC_RMS_WARNING:
            score -= 15
        if acc > config.ACC_RMS_ALARM:
            score -= 20

        # CREST FACTOR
        if crest > config.CREST_WARNING:
            score -= 15
        if crest > config.CREST_ALARM:
            score -= 20

        # HIGH FREQUENCY
        if hf > config.HF_WARNING:
            score -= 15
        if hf > config.HF_ALARM:
            score -= 15

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


