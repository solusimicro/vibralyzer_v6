from compat import PLATFORM

if PLATFORM == "ESP32":
    import network
    import config
    import time


    class WiFiEngine:

        def __init__(self):
            self.wlan = network.WLAN(network.STA_IF)
            self.wlan.active(True)

        def connect(self):
            if not self.wlan.isconnected():
                self.wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

                timeout = 10
                while not self.wlan.isconnected() and timeout > 0:
                    time.sleep(1)
                    timeout -= 1

        def ensure(self):
            if not self.wlan.isconnected():
                self.connect()


