# mqtt_client.py

import json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

client = mqtt.Client()

def connect():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

def publish(payload):
    client.publish(MQTT_TOPIC, json.dumps(payload))

