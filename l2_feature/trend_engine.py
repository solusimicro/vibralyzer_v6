import numpy as np

class TrendEngine:
    """
    Menghitung slope dan degradasi.
    Deterministic linear regression.
    """

    @staticmethod
    def calculate_slope(data):
        if len(data) < 2:
            return 0.0
        x = np.arange(len(data))
        y = np.array(data)
        slope = np.polyfit(x, y, 1)[0]
        return float(slope)

    def analyze(self, buffer_data):
        vel_slope = self.calculate_slope(buffer_data["vel_rms"])
        crest_slope = self.calculate_slope(buffer_data["crest"])
        hf_slope = self.calculate_slope(buffer_data["hf"])
        health_decay = self.calculate_slope(buffer_data["health"])

        return {
            "vel_slope": vel_slope,
            "crest_slope": crest_slope,
            "hf_slope": hf_slope,
            "health_decay": health_decay,
        }
