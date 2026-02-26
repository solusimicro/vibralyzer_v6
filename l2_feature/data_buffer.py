from collections import deque

class DataBuffer:
    """
    Menyimpan rolling window data per asset per device.
    Digunakan oleh TrendEngine.
    ML-ready: data bisa langsung diexport.
    """

    def __init__(self, window_size=20):
        self.window_size = window_size
        self.buffer = {}  # key: "asset_id_device_id"

    def _make_key(self, asset_id, device_id):
        return f"{asset_id}_{device_id}"

    def update(self, asset_id, device_id, payload):
        key = self._make_key(asset_id, device_id)
        if key not in self.buffer:
            self.buffer[key] = {
                "vel_rms": deque(maxlen=self.window_size),
                "crest": deque(maxlen=self.window_size),
                "hf": deque(maxlen=self.window_size),
                "health": deque(maxlen=self.window_size),
            }

        self.buffer[key]["vel_rms"].append(payload["vel_rms"])
        self.buffer[key]["crest"].append(payload["crest"])
        self.buffer[key]["hf"].append(payload["hf"])
        self.buffer[key]["health"].append(payload["health_index"])

    def get(self, asset_id, device_id):
        key = self._make_key(asset_id, device_id)
        return self.buffer.get(key, None)

