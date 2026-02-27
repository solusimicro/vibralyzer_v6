# main.py
import time
import gc
import config

from state_machine import StateMachine
from signal_engine import SignalEngine
from feature_engine import FeatureEngine
from mqtt_engine import MQTTEngine
from usb_engine import USBEngine
from l1_logic import L1Logic


def main():

    sm = StateMachine()
    sig = SignalEngine()
    feat = FeatureEngine(config.FS)
    mqtt = MQTTEngine()
    usb = USBEngine(config.SERIAL_BAUDRATE)
    logic = L1Logic()

    sm.set("BOOT")

    # ==========================
    # COMMUNICATION DECISION
    # ==========================
    online = False

    if config.COMM_MODE == "USB_ONLY":
        online = False

    elif config.COMM_MODE == "MQTT_ONLY":
        online = mqtt.connect()

    else:  # AUTO
        online = mqtt.connect()

    if online:
        sm.set("ONLINE")
    else:
        sm.set("OFFLINE_USB")

    sm.set("RUN")

    # ==========================
    # MAIN LOOP
    # ==========================
    while True:

        buffer = sig.sample()
        buffer = sig.preprocess(buffer)

        # 3️⃣ Feature Extraction
        features = {
            "acc_rms": feat.rms(buffer),
            "vel_rms": feat.vel_rms(buffer),
            "crest": feat.crest(buffer),
            "hf": feat.hf_rms(buffer),
        }

        # 4️⃣ Decision Logic
        decision = logic.evaluate(features)

        # 5️⃣ Payload
        payload = {
            "site": config.SITE,
            "asset": config.ASSET,
            "device": config.DEVICE_ID,
            "firmware": config.FIRMWARE_VERSION,

            "acc_rms": features["acc_rms"],
            "vel_rms": features["vel_rms"],
            "crest": features["crest"],
            "hf": features["hf"],

            "iso_zone": decision["iso_zone"],
            "health_index": decision["health_index"],
            "state": decision["state"]
        }

        # Publish
        if online:
            try:
                mqtt.publish(payload)
            except:
                online = False
                sm.set("OFFLINE_USB")
                usb.publish(payload)
        else:
            usb.publish(payload)

        gc.collect()
        time.sleep(config.LOOP_DELAY_SEC)


if __name__ == "__main__":
    main()
