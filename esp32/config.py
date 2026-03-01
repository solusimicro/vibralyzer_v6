# ==========================================================
# SYSTEM IDENTITY (MANDATORY FOR MQTT PAYLOAD)
# ==========================================================
SITE  = "SITE_A"
ASSET = "PUMP_01"
DEVICE_ID = "EDGE_001"
FIRMWARE_VERSION = "1.0.0"
# ==========================================================
# SYSTEM MODE
# ==========================================================
MODE = "PC"      # PC | ESP32

# ==========================================================
# SAMPLING CONFIG
# ==========================================================
FS = 1024        # Sampling frequency (Hz)
N  = 1024        # Window size (must be power of 2)

# ==========================================================
# COMMUNICATION MODE
# ==========================================================
COMM_MODE = "AUTO"            # AUTO | MQTT_ONLY | USB_ONLY
NETWORK_PRIORITY = "LAN_FIRST"  # LAN_FIRST | WIFI_FIRST

# ==========================================================
# WIFI CONFIG
# ==========================================================
WIFI_SSID = "Factory_WiFi"
WIFI_PASSWORD = "12345678"

# ==========================================================
# ETHERNET CONFIG
# ==========================================================
ETHERNET_ENABLED = True
ETH_DHCP = True
ETH_IP = "192.168.1.50"
ETH_GATEWAY = "192.168.1.1"
ETH_SUBNET = "255.255.255.0"

# ==========================================================
# MQTT CONFIG
# ==========================================================
MQTT_BROKER = "192.168.1.10"
MQTT_PORT   = 1883
CLIENT_ID   = "EDGE_PUMP_01"

# Topic akan dibuat dinamis di main.py
MQTT_BASE_TOPIC = "vibration/l1"

# ==========================================================
# USB CONFIG (commissioning only)
# ==========================================================
SERIAL_BAUDRATE = 115200

# ==========================================================
# ISO 10816 Velocity Threshold (mm/s RMS)
# Small machine baseline
# ==========================================================

# VELOCITY (mm/s RMS)
VEL_WARNING = 2.8
VEL_ALARM   = 4.5

# ACC RMS (g)
ACC_RMS_WARNING = 0.3
ACC_RMS_ALARM   = 0.5

# CREST FACTOR
CREST_WARNING = 3.0
CREST_ALARM   = 4.5

# HIGH FREQUENCY RMS
HF_WARNING = 0.2
HF_ALARM   = 0.35

# ==========================================================
# HEALTH INDEX WEIGHTING (for future ML-ready scoring)
# ==========================================================
WEIGHT_ACC   = 0.4
WEIGHT_VEL   = 0.3
WEIGHT_CREST = 0.2
WEIGHT_HF    = 0.1
