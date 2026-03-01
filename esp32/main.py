# ==========================================
# Vibralyzer v6 - L1 Edge Final
# ==========================================

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

    print("=== MAIN START ===")

    # --------------------------------------
    # INIT SECTION
    # --------------------------------------
    print("INIT SM")
    sm = StateMachine()

    print("INIT SIGNAL")
    sig = SignalEngine()

    print("INIT FEATURE")
    feat = FeatureEngine(config.FS)

    print("INIT MQTT")
    mqtt = MQTTEngine()

    print("INIT USB")
    usb = USBEngine(config.SERIAL_BAUDRATE)

    print("INIT LOGIC")
    logic = L1Logic()

    print("ALL INIT DONE")

    # --------------------------------------
    # COMMUNICATION DECISION
    # --------------------------------------
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

    print("ENTER RUN LOOP")

    # --------------------------------------
    # MAIN LOOP
    # --------------------------------------
    while True:

        try:
            # 1️⃣ Generate signal
            raw = sig.sample()

            # 2️⃣ Conditioning (in-place → hemat memory)
            sig.remove_dc()
            sig.apply_window()

            # 3️⃣ Integrate to velocity (mm/s)
            velocity = sig.integrate_velocity()

            # 4️⃣ Feature extraction
            acc_rms = feat.rms(raw)
            vel_rms = feat.rms(velocity)
            crest   = feat.crest(raw)
            hf      = feat.hf_rms(raw)

            # 5️⃣ Decision logic
            features = {
                "acc_rms": acc_rms,
                "vel_rms": vel_rms,
                "crest": crest,
                "hf": hf
            }

            decision = logic.evaluate(features)

            # 6️⃣ Debug print
            print(
                "ACC:", round(acc_rms, 3),
                "VEL:", round(vel_rms, 3),
                "STATE:", decision["state"]
            )

            # 7️⃣ Payload
            payload = {
                "site": config.SITE,
                "asset": config.ASSET,
                "device": config.DEVICE_ID,
                "firmware": config.FIRMWARE_VERSION,

                "acc_rms": acc_rms,
                "vel_rms": vel_rms,
                "crest": crest,
                "hf": hf,

                "iso_zone": decision["iso_zone"],
                "health_index": decision["health_index"],
                "state": decision["state"]
            }

            # 8️⃣ Publish
            if online:
                try:
                    mqtt.publish(payload)
                except:
                    online = False
                    sm.set("OFFLINE_USB")
                    usb.publish(payload)
            else:
                usb.publish(payload)

            # 9️⃣ Memory cleanup (MicroPython safe)
            gc.collect()
            time.sleep(1)

        except Exception as e:
            print("MAIN LOOP ERROR:", e)
            time.sleep(2)


# ==========================================
if __name__ == "__main__":
    main()


