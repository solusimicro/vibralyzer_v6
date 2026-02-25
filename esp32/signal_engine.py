import config
from compat import np


class SignalEngine:

    def __init__(self):
        self.fs = config.FS
        self.window_size = config.WINDOW_SIZE
        self.buffer = np.zeros(self.window_size)

    def sample(self):
        # PC simulation
        t = np.arange(self.window_size) / self.fs
        self.buffer[:] = 0.15 * np.sin(2*np.pi*30*t)
        return self.buffer

    def preprocess(self, buffer):
        return buffer - np.mean(buffer)



