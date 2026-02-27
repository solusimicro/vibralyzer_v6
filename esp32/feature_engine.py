from compat import np


class FeatureEngine:

    def __init__(self, fs):
        self.fs = fs

    # -------------------------
    # Remove DC
    # -------------------------
    def remove_dc(self, sig):
        return sig - np.mean(sig)

    # -------------------------
    # RMS
    # -------------------------
    def rms(self, sig):
        return float(np.sqrt(np.mean(sig * sig)))

    # -------------------------
    # Crest Factor
    # -------------------------
    def crest(self, sig):
        r = self.rms(sig)
        peak = float(np.max(np.abs(sig)))
        return peak / r if r else 0

    # -------------------------
    # HF RMS (differentiation)
    # -------------------------
    def hf_rms(self, sig):
        diff = np.diff(sig)
        return float(np.sqrt(np.mean(diff * diff)))

    # -------------------------
    # Velocity RMS
    # -------------------------
    def vel_rms(self, sig):
        sig = self.remove_dc(sig)
        vel = np.cumsum(sig) / self.fs
        return float(np.sqrt(np.mean(vel * vel)))




