from ulab import numpy as np

class CV2_Camera():
    def __init__(self, buffer_size):
        self.buffer = np.zeros(buffer_size, dtype=np.uint8)
