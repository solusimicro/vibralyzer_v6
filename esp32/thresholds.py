# thresholds.py

from config import ACC_RMS_ALARM, HF_RMS_ALARM, CREST_ALARM

def evaluate(acc_rms, hf_rms, crest):
    state = "NORMAL"

    if acc_rms > ACC_RMS_ALARM:
        state = "ALARM"
    elif hf_rms > HF_RMS_ALARM:
        state = "WARNING"
    elif crest > CREST_ALARM:
        state = "EARLY_WARNING"

    return state
