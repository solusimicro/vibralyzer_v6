import time, gc, json, config
from signal_engine import SignalEngine
from feature_engine import FeatureEngine
from l1_logic import L1Logic
from mqtt_engine import MQTTEngine
from usb_engine import USBEngine
from network_engine import NetworkEngine
from state_machine import StateMachine

def main():
    print("=== VIBRALYZER V6 PC-SAFE ===")

    net = NetworkEngine()
    sm = StateMachine()
    sig = SignalEngine()
    feat = FeatureEngine(config.FS)
    mqtt = MQTTEngine()
    usb = USBEngine(config.SERIAL_BAUDRATE)
    logic = L1Logic()

    # connect network + mqtt
    network_ready = net.connect()
    online = mqtt.connect() if network_ready else False
    sm.set("ONLINE" if online else "OFFLINE_USB")
    sm.set("RUN")

    while True:
        try:
            raw = sig.sample()
            sig.remove_dc()
            sig.apply_window()
            velocity = sig.integrate_velocity()

            acc_rms = feat.rms(raw)
            vel_rms = feat.rms(velocity)
            crest = feat.crest(raw)
            hf = feat.hf_rms(raw)

            decision = logic.evaluate({
                "acc_rms": acc_rms,
                "vel_rms": vel_rms,
                "crest": crest,
                "hf": hf
            })

            payload = {
                "timestamp": int(time.time()),
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

            # publish
            if not mqtt.publish(payload):
                usb.publish(payload)

            gc.collect()
            time.sleep(1)

        except Exception as e:
            print("MAIN LOOP ERROR:", e)
            time.sleep(2)

if __name__ == "__main__":
    main()



