# usb_engine.py
import json
import sys

class USBEngine:

    def __init__(self, baudrate=115200):
        self.baudrate = baudrate

    def publish(self, payload):
        print(json.dumps(payload))
        sys.stdout.flush()
