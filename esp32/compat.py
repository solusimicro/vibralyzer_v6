# compat.py
# Cross-platform compatibility flags

try:
    import machine
    PLATFORM = "ESP32"
except ImportError:
    PLATFORM = "PC"
