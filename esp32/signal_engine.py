# ==========================================
# Cross Platform NumPy Compatibility
# ==========================================
try:
    from ulab import numpy as np
    PLATFORM = "ESP32"
except ImportError:
    import numpy as np
    PLATFORM = "PC"

from config import FS, N


class SignalEngine:

    def __init__(self,
                 fault_type="UNBALANCE",
                 growth="linear",
                 start_severity=0.05,
                 max_severity=0.6,
                 steps_to_fail=300):

        self.fault_type = fault_type
        self.growth = growth

        self.start_severity = start_severity
        self.max_severity = max_severity
        self.steps_to_fail = steps_to_fail

        self.step = 0
        self.severity = start_severity

        self.buffer = np.zeros(N)

        self.window = 0.5 * (1 - np.cos(
            2*np.pi*np.arange(N)/(N-1)
        ))

    # ==========================================
    # UPDATE SEVERITY (Progressive Growth)
    # ==========================================
    def update_severity(self):

        if self.growth == "linear":
            delta = (self.max_severity - self.start_severity) / self.steps_to_fail
            self.severity += delta

        elif self.growth == "exponential":
            k = 5 / self.steps_to_fail
            self.severity = self.start_severity * np.exp(k * self.step)

        if self.severity > self.max_severity:
            self.severity = self.max_severity

        self.step += 1

    # ==========================================
    # SAMPLE GENERATOR
    # ==========================================
    def sample(self):

        self.update_severity()

        t = np.arange(N) / FS

        base = 0.05 * np.sin(2*np.pi*10*t)

        if self.fault_type == "UNBALANCE":
            fault = self.severity * np.sin(2*np.pi*30*t)

        elif self.fault_type == "MISALIGNMENT":
            fault = self.severity * np.sin(2*np.pi*60*t)

        elif self.fault_type == "BEARING":
            fault = self.severity * np.sin(2*np.pi*250*t)

        elif self.fault_type == "LOOSENESS":
            fault = self.severity * (
                np.sin(2*np.pi*30*t) +
                np.sin(2*np.pi*90*t)
            )

        else:
            fault = 0

        noise = 0.02 * np.random.randn(N)

        self.buffer[:] = base + fault + noise

        return self.buffer

    # ==========================================
    def remove_dc(self):
        mean = np.mean(self.buffer)
        self.buffer[:] -= mean

    # ==========================================
    def apply_window(self):
        self.buffer[:] *= self.window

    # ==========================================
    def integrate_velocity(self):
        dt = 1 / FS
        velocity = np.cumsum(self.buffer) * dt

        # Convert m/s → mm/s (ISO standard)
        velocity = velocity * 1000

        return velocity

