import json
import config
from compat import PLATFORM

if PLATFORM == "ESP32":
    from umqtt.simple import MQTTClient
else:
    import paho.mqtt.client as mqtt


class MQTTEngine:

    def __init__(self):

        if PLATFORM == "ESP32":
            self.client = MQTTClient(
                config.DEVICE,
                config.MQTT_BROKER,
                port=config.MQTT_PORT
            )
        else:
            self.client = mqtt.Client(client_id=config.DEVICE)

    def connect(self):
        if PLATFORM == "ESP32":
            self.client.connect()
        else:
            self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            self.client.loop_start()

    def publish(self, payload):

        topic = f"vibration/l1/{config.SITE}/{config.ASSET}/{config.DEVICE}"
        self.client.publish(topic, json.dumps(payload))

        if PLATFORM == "PC":
            print(topic, payload)








