# config.py

MODE = "PC"        # change to "ESP32" when deploying

FS = 1024
WINDOW_SIZE = 1024

ACC_RMS_ALARM = 0.3
CREST_ALARM = 4.0

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vibration/l1/SITE_A/PUMP_01"
CLIENT_ID = "EDGE_PUMP_01"

