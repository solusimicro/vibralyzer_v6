try:
    from ulab import numpy as np
    PLATFORM = "ESP32"
except ImportError:
    import numpy as np
    PLATFORM = "PC"

