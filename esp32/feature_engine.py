# feature_engine.py

from compat import np

class FeatureEngine:

    def rms(self, sig):
        return float(np.sqrt(np.mean(sig*sig)))

    def crest(self, sig):
        r = self.rms(sig)
        p = float(np.max(np.abs(sig)))
        return p/r if r else 0
