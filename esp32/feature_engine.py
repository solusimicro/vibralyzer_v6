from ulab import numpy as np

class FeatureEngine:

    def rms(self, sig):
        return float(np.sqrt(np.mean(sig*sig)))

    def crest(self, sig):
        r = self.rms(sig)
        peak = float(np.max(np.abs(sig)))
        return peak/r if r else 0

    def hf_rms(self, sig):
        # high-pass sederhana via differentiation
        diff = np.diff(sig)
        return float(np.sqrt(np.mean(diff*diff)))

