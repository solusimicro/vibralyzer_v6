import json
import config

if config.COMM_MODE in ("AUTO", "MQTT_ONLY"):
    import paho.mqtt.client as mqtt


class MQTTEngine:

    def __init__(self):

        self.online = False

        if config.COMM_MODE in ("AUTO", "MQTT_ONLY"):
            self.client = mqtt.Client(
                client_id=config.DEVICE_ID,
                protocol=mqtt.MQTTv311
            )

    # ---------------------------------
    # CONNECT
    # ---------------------------------
    def connect(self):

        try:
            self.client.connect(
                config.MQTT_BROKER,
                config.MQTT_PORT,
                60
            )
            self.client.loop_start()
            self.online = True
            return True

        except Exception as e:
            print("MQTT CONNECT ERROR:", e)
            self.online = False
            return False

    # ---------------------------------
    # PUBLISH
    # ---------------------------------
    def publish(self, payload):

        if not self.online:
            return False

        topic = f"vibration/l1/{config.SITE}/{config.ASSET}/{config.DEVICE_ID}"

        try:
            self.client.publish(topic, json.dumps(payload))
            return True
        except Exception as e:
            print("MQTT PUBLISH ERROR:", e)
            self.online = False
            return False


