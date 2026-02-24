# sampler.py

import numpy as np
from config import FS, WINDOW_SIZE

def get_window():
    t = np.arange(WINDOW_SIZE) / FS

    signal = (
        0.15 * np.sin(2*np.pi*30*t) +
        0.05 * np.sin(2*np.pi*120*t) +
        0.02 * np.random.randn(WINDOW_SIZE)
    )

    return signal
