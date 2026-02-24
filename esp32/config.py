# config.py

FS = 2048                 # sampling frequency
WINDOW_SIZE = 2048        # 1 second window
HF_CUTOFF = 200           # Hz (high frequency threshold)

ACC_RMS_ALARM = 0.3       # g
HF_RMS_ALARM = 0.1        # g
CREST_ALARM = 4.0

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vibration/l1/SITE_A/PUMP_01"
