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
            try:
                if not self.wlan.isconnected():

                    print("WiFi: Connecting...")

                    self.wlan.connect(
                        config.WIFI_SSID,
                        config.WIFI_PASSWORD
                    )

                    timeout = 10

                    while not self.wlan.isconnected() and timeout > 0:
                        time.sleep(1)
                        timeout -= 1

                    if not self.wlan.isconnected():
                        print("WiFi: Connection Timeout")
                        return False

                print("WiFi: Connected →", self.wlan.ifconfig())
                return True

            except OSError as e:
                print("WiFi OSError:", e)
                return False

            except Exception as e:
                print("WiFi Unknown Error:", e)
                return False

        def ensure(self):
            if not self.wlan.isconnected():
                self.connect()


