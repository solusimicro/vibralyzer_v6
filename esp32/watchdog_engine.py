import time
import config
from compat import PLATFORM

try:
    import machine
except ImportError:
    machine = None


class WatchdogEngine:

    def __init__(self):
        self.last = time.time()

    def kick(self):
        self.last = time.time()

    def check(self):
        if time.time() - self.last > config.WDT_TIMEOUT_SEC:
            print("WATCHDOG RESET")
            if PLATFORM == "ESP32" and machine:
                machine.reset()
            else:
                raise SystemExit

