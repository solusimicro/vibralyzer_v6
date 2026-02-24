# main.py

import time
from sampler import get_window
from preprocess import remove_dc, hanning_window
from features import acc_rms, hf_rms, crest_factor
from thresholds import evaluate
from mqtt_client import connect, publish

def run():
    connect()

    while True:
        signal = get_window()
        signal = remove_dc(signal)
        signal = hanning_window(signal)

        rms = acc_rms(signal)
        hf = hf_rms(signal)
        crest = crest_factor(signal)

        state = evaluate(rms, hf, crest)

        payload = {
            "acc_rms_g": rms,
            "acc_hf_rms_g": hf,
            "crest_factor": crest,
            "state": state
        }

        publish(payload)
        print(payload)

        time.sleep(1)

if __name__ == "__main__":
    run()
