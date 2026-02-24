# preprocess.py

import numpy as np

def remove_dc(signal):
    return signal - np.mean(signal)

def hanning_window(signal):
    N = len(signal)
    window = 0.5 * (1 - np.cos(2*np.pi*np.arange(N)/(N-1)))
    return signal * window
