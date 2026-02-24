from config import *

def evaluate(acc, vel, crest, hf):

    score = 0

    if acc > ACC_WARNING:
        score += 1
    if acc > ACC_ALARM:
        score += 1

    if vel > VEL_WARNING:
        score += 1
    if vel > VEL_ALARM:
        score += 1

    if crest > CREST_LIMIT:
        score += 1

    if hf > HF_LIMIT:
        score += 1

    if score <= 1:
        return "NORMAL"
    elif score <= 3:
        return "WARNING"
    elif score <= 4:
        return "ALARM"
    else:
        return "CRITICAL"
