# mqtt_engine.py
import config, json

# Cross-platform MQTT
try:
    if config.MODE == "ESP32":
        from umqtt.simple import MQTTClient
    else:
        import paho.mqtt.client as paho
except ImportError as e:
    print("MQTT module not found:", e)

class MQTTEngine:
    def __init__(self):
        self.connected = False
        self.mode = config.MODE

        if self.mode == "ESP32":
            self.client = MQTTClient(config.CLIENT_ID, config.MQTT_BROKER, port=config.MQTT_PORT)
        else:
            self.client = paho.Client(client_id=config.CLIENT_ID)

    def connect(self):
        try:
            if self.mode == "ESP32":
                self.client.connect()
            else:
                self.client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
                self.client.loop_start()
            self.connected = True
            print("MQTT CONNECTED")
            return True
        except Exception as e:
            print("MQTT connect failed:", e)
            self.connected = False
            return False

    def publish(self, payload):
        if not self.connected:
            return False

        topic = f"{config.MQTT_BASE_TOPIC}/{config.SITE}/{config.ASSET}/{config.DEVICE_ID}"
        msg = json.dumps(payload)

        try:
            if self.mode == "ESP32":
                self.client.publish(topic, msg)
            else:
                self.client.publish(topic, msg)
            print("MQTT PUBLISH:", topic, msg)  # debug
            return True
        except Exception as e:
            print("MQTT publish failed:", e)
            self.connected = False
            return False


