# main.py

import time
import gc
from state_machine import StateMachine
from signal_engine import SignalEngine
from feature_engine import FeatureEngine
from mqtt_engine import MQTTEngine
from config import ACC_RMS_ALARM, CREST_ALARM

def main():

    sm = StateMachine()
    sig = SignalEngine()
    feat = FeatureEngine()
    mqtt = MQTTEngine()

    sm.set("CONNECT")
    mqtt.connect()

    sm.set("RUN")

    while True:

        buffer = sig.sample()
        buffer = sig.preprocess()

        acc = feat.rms(buffer)
        crest = feat.crest(buffer)

        state = "NORMAL"

        if acc > ACC_RMS_ALARM:
            state = "ALARM"
        elif crest > CREST_ALARM:
            state = "EARLY_WARNING"

        payload = {
            "acc_rms_g": acc,
            "crest_factor": crest,
            "state": state
        }

        mqtt.publish(payload)

        gc.collect()
        time.sleep(1)


if __name__ == "__main__":
    main()

