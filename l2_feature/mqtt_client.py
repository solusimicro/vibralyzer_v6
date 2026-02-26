import json
import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self, host, port, topic_sub, on_message_callback):
        self.client = mqtt.Client()
        self.client.on_message = on_message_callback
        self.client.connect(host, port)
        self.client.subscribe(topic_sub)

    def loop_forever(self):
        self.client.loop_forever()

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload), qos=1)
