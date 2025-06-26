from .hm01b0 import HM01B0
from .dvp_rp2_pio import DVP_RP2_PIO

class HM01B0_PIO(HM01B0, DVP_RP2_PIO):
    def __init__(
        self,
        i2c,
        pin_d0,
        pin_vsync,
        pin_hsync,
        pin_pclk,
        pin_xclk = None,
        sm_id = 0,
        num_data_pins = 1,
        i2c_address = 0x24,
    ):
        # Call both parent constructors
        HM01B0.__init__(self, i2c, i2c_address, num_data_pins)
        DVP_RP2_PIO.__init__(self, pin_d0, pin_vsync, pin_hsync, pin_pclk, pin_xclk, sm_id, num_data_pins)

    def open(self):
        self.active(True)

    def release(self):
        self.active(False)
