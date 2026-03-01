import config
import time

try:
    import network
except ImportError:
    network = None


class NetworkEngine:

    def __init__(self):
        self.active = None

    def connect(self):

        if config.NETWORK_MODE == "DUAL":
            if self.connect_ethernet():
                self.active = "ETHERNET"
                return True

            if self.connect_wifi():
                self.active = "WIFI"
                return True

            return False

        elif config.NETWORK_MODE == "ETHERNET":
            return self.connect_ethernet()

        elif config.NETWORK_MODE == "WIFI":
            return self.connect_wifi()

    def connect_wifi(self):
        if not network:
            return False

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

        return wlan.isconnected()

    def connect_ethernet(self):
        # Stub for W5500
        # Real implementation uses machine.SPI
        return False
