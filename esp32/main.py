import time, gc, json
import config
from signal_engine import SignalEngine
from feature_engine import FeatureEngine
from l1_logic import L1Logic
from mqtt_engine import MQTTEngine

def main():
    print("=== VIBRALYZER V6 PC-SAFE START ===")

    sig = SignalEngine()
    feat = FeatureEngine(config.FS)
    logic = L1Logic()
    mqtt = MQTTEngine()

    # Connect to broker localhost
    online = mqtt.connect()

    while True:
        raw = sig.sample()
        sig.remove_dc()
        sig.apply_window()
        vel = sig.integrate_velocity()

        features = {
            "acc_rms": feat.rms(raw),
            "vel_rms": feat.rms(vel),
            "crest": feat.crest(raw),
            "hf": feat.hf_rms(raw)
        }

        decision = logic.evaluate(features)

        payload = {
            "timestamp": time.time(),
            "site": config.SITE,
            "asset": config.ASSET,
            "device": config.DEVICE_ID,
            "firmware": config.FIRMWARE_VERSION,
            **features,
            "iso_zone": decision["iso_zone"],
            "health_index": decision["health_index"],
            "state": decision["state"]
        }

        if online:
            mqtt.publish(payload)
        else:
            print("MQTT OFFLINE, payload:", json.dumps(payload))

        gc.collect()
        time.sleep(1)

if __name__ == "__main__":
    main()
