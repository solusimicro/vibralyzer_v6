# signal_engine.py

from compat import np
from config import FS, WINDOW_SIZE

class SignalEngine:

    def __init__(self):
        self.buffer = np.zeros(WINDOW_SIZE)
        self.window = 0.5 * (1 - np.cos(
            2*np.pi*np.arange(WINDOW_SIZE)/(WINDOW_SIZE-1)
        ))

    def sample(self):
        # PC simulation
        t = np.arange(WINDOW_SIZE)/FS
        self.buffer[:] = (
            0.15*np.sin(2*np.pi*30*t)
        )
        return self.buffer

    def preprocess(self):
        mean = np.mean(self.buffer)
        self.buffer[:] = self.buffer - mean
        self.buffer[:] = self.buffer * self.window
        return self.buffer

