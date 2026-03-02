import config

# MicroPython safe import
try:
    import machine
except ImportError:
    machine = None

import time

class WatchdogEngine:
    def __init__(self):
        self.last = time.time()
        # ESP32 WDT
        if machine:
            self.wdt = machine.WDT(timeout=config.WDT_TIMEOUT_SEC*1000)

    def kick(self):
        self.last = time.time()
        if hasattr(self, "wdt"):
            self.wdt.feed()

    def check(self):
        # fallback PC: exit if timeout
        if time.time() - self.last > config.WDT_TIMEOUT_SEC:
            print("WATCHDOG TIMEOUT")
            if machine:
                machine.reset()
            else:
                raise SystemExit

