import config, time
try:
    import network
except ImportError:
    network = None

class NetworkEngine:
    def __init__(self):
        self.active = None

    def connect(self):
        if config.NETWORK_PRIORITY == "LAN_FIRST":
            if config.ETHERNET_ENABLED and self.connect_ethernet():
                self.active = "ETHERNET"
                return True
            if self.connect_wifi():
                self.active = "WIFI"
                return True
        else:
            if self.connect_wifi():
                self.active = "WIFI"
                return True
            if config.ETHERNET_ENABLED and self.connect_ethernet():
                self.active = "ETHERNET"
                return True
        return False

    def connect_wifi(self):
        if not network: return False
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print("NETWORK -> WIFI CONNECTED")
            return True
        return False

    def connect_ethernet(self):
        # implement W5500 or LAN PHY
        print("NETWORK -> ETHERNET (stub)")
        return False


