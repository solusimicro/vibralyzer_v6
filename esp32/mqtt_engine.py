import config
import json

if config.MODE == "ESP32":
    from umqtt.simple import MQTTClient
else:
    import paho.mqtt.client as paho


class MQTTEngine:

    def __init__(self):

        self.connected = False

        if config.MODE == "ESP32":
            self.client = MQTTClient(
                config.CLIENT_ID,
                config.MQTT_BROKER,
                port=config.MQTT_PORT
            )
        else:
            self.client = paho.Client()
    
    def connect(self):
        try:
            if config.MODE == "ESP32":
                self.client.connect()
            else:
                self.client.connect(
                    config.MQTT_BROKER,
                    config.MQTT_PORT,
                    60
                )
                self.client.loop_start()

            self.connected = True
            return True

        except Exception as e:
            print("MQTT connect failed:", e)
            self.connected = False
            return False

    def publish(self, payload):

        if not self.connected:
            return False

        topic = config.MQTT_BASE_TOPIC

        msg = json.dumps(payload)

        if config.MODE == "ESP32":
            self.client.publish(topic, msg)
        else:
            self.client.publish(topic, msg)

        return True


