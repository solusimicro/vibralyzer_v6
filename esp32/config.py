# ==========================================================
# VIBRALYZER L1 EDGE CONFIG
# 1 Sensor = 1 ESP32 = 1 Device
# Industrial Grade Locked Configuration
# ==========================================================

# ===== DEVICE IDENTITY =====
SITE = "SITE_A"
ASSET = "PUMP_01"
DEVICE_ID = "EDGE_PUMP_01"
FIRMWARE_VERSION = "L1_v2.0"

# ===== SIGNAL CONFIG =====
FS = 1024
WINDOW_SIZE = 1024

# ===== THRESHOLDS =====
ACC_RMS_ALARM = 0.3
VEL_WARNING = 2.8
VEL_ALARM = 4.5
CREST_LIMIT = 4.0
HF_LIMIT = 0.1

# ===== WIFI =====
WIFI_SSID = "YOUR_SSID"
WIFI_PASSWORD = "YOUR_PASSWORD"

# ===== MQTT =====
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

# Topic generated automatically
MQTT_TOPIC = f"vibration/l1/{SITE}/{ASSET}/{DEVICE_ID}"

# ===== WATCHDOG =====
WDT_TIMEOUT_SEC = 8
LOOP_DELAY_SEC = 1

# ===== COMMUNICATION MODE =====
# AUTO        → Detect platform
# MQTT_ONLY   → Force MQTT
# USB_ONLY    → Force Serial Output
COMM_MODE = "AUTO"
SERIAL_BAUDRATE = 115200

