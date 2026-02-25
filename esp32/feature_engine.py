from compat import np
import config


class FeatureEngine:

    def __init__(self):
        self.fs = config.FS

    def rms(self, sig):
        return float(np.sqrt(np.mean(sig * sig)))

    def crest(self, sig):
        r = self.rms(sig)
        peak = float(np.max(np.abs(sig)))
        return peak / r if r else 0

    def hf_rms(self, sig):
        diff = np.diff(sig)
        return float(np.sqrt(np.mean(diff * diff)))

    def vel_rms(self, sig):
        sig = sig - np.mean(sig)
        vel = np.cumsum(sig) / self.fs
        return float(np.sqrt(np.mean(vel * vel)))



