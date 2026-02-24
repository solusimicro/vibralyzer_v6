# features.py

import numpy as np
from config import FS, HF_CUTOFF

def acc_rms(signal):
    return np.sqrt(np.mean(signal**2))

def crest_factor(signal):
    rms = acc_rms(signal)
    peak = np.max(np.abs(signal))
    return peak / rms if rms != 0 else 0

def hf_rms(signal):
    # FFT-based high frequency RMS
    N = len(signal)
    freqs = np.fft.rfftfreq(N, 1/FS)
    spectrum = np.abs(np.fft.rfft(signal))

    hf_mask = freqs >= HF_CUTOFF
    hf_energy = np.sqrt(np.sum((spectrum[hf_mask])**2) / len(spectrum[hf_mask]))
    return hf_energy
