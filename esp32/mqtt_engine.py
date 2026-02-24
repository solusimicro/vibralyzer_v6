# mqtt_engine.py

from config import MODE, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, CLIENT_ID

if MODE == "ESP32":
    from umqtt.simple import MQTTClient
else:
    import paho.mqtt.client as mqtt


class MQTTEngine:

    def __init__(self):

        if MODE == "ESP32":
            self.client = MQTTClient(CLIENT_ID, MQTT_BROKER)

        else:
            self.client = mqtt.Client(
                client_id=CLIENT_ID,
                protocol=mqtt.MQTTv311,
                transport="tcp",
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2
            )

    def connect(self):
        if MODE == "ESP32":
            self.client.connect()
        else:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)

    def publish(self, payload):

        import json

        self.client.publish(MQTT_TOPIC, json.dumps(payload))
        print("MQTT:", payload)




