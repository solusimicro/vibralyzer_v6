import time
import gc
import config

from state_machine import StateMachine
from signal_engine import SignalEngine
from feature_engine import FeatureEngine
from l1_logic import L1Logic
from mqtt_engine import MQTTEngine
from watchdog_engine import WatchdogEngine
from compat import PLATFORM

if PLATFORM == "ESP32":
    from wifi_engine import WiFiEngine


def main():

    sm = StateMachine()
    sig = SignalEngine()
    feat = FeatureEngine()
    logic = L1Logic()
    mqtt = MQTTEngine()
    wd = WatchdogEngine()

    sm.set("BOOT")

    if PLATFORM == "ESP32":
        wifi = WiFiEngine()
        wifi.connect()

    sm.set("CONNECT")
    mqtt.connect()
    sm.set("RUN")

    while True:

        wd.kick()

        buffer = sig.sample()
        buffer = sig.preprocess(buffer)

        features = {
            "acc_rms": feat.rms(buffer),
            "vel_rms": feat.vel_rms(buffer),
            "crest": feat.crest(buffer),
            "hf": feat.hf_rms(buffer)
        }

        iso, health, state = logic.evaluate(features)

        payload = {
            "site": config.SITE,
            "asset": config.ASSET,
            "device": config.DEVICE,
            "firmware": config.FIRMWARE,
            **features,
            "iso_zone": iso,
            "health_index": health,
            "state": state
        }

        mqtt.publish(payload)

        wd.check()
        gc.collect()
        time.sleep(config.LOOP_DELAY_SEC)


if __name__ == "__main__":
    main()

