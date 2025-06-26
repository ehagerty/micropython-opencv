import rp2
from machine import Pin, PWM

class DVP_RP2_PIO():
    def __init__(
        self,
        pin_d0,
        pin_vsync,
        pin_hsync,
        pin_pclk,
        pin_xclk,
        sm_id,
        num_data_pins
    ):
        self.pin_d0 = pin_d0
        self.pin_vsync = pin_vsync
        self.pin_hsync = pin_hsync
        self.pin_pclk = pin_pclk
        self.pin_xclk = pin_xclk
        self.sm_id = sm_id

        for i in range(num_data_pins):
            Pin(pin_d0+i, Pin.IN)
        Pin(pin_vsync, Pin.IN)
        Pin(pin_hsync, Pin.IN)
        Pin(pin_pclk, Pin.IN)

        if self.pin_xclk is not None:
            self.xclk = PWM(Pin(pin_xclk))
            self.xclk.freq(25_000_000)
            # self.xclk.freq(15_000_000) # Test for OV5640
            self.xclk.duty_u16(32768)

        self.start_pio_dma(num_data_pins)

    def start_pio_dma(self, num_data_pins):
        program = self._pio_read_dvp
        # Mask in the GPIO pins
        program[0][0] |= self.pin_hsync & 0x1F
        program[0][1] |= self.pin_pclk & 0x1F
        program[0][3] |= self.pin_pclk & 0x1F

        # Mask in the number of data pins
        program[0][2] &= 0xFFFFFFE0
        program[0][2] |= num_data_pins

        self.sm = rp2.StateMachine(
            self.sm_id,
            program,
            in_base = self.pin_d0
        )
        self.sm.active(1)

        self.dma = rp2.DMA()
        req_num = ((self.sm_id // 4) << 3) + (self.sm_id % 4) + 4
        dma_ctrl = self.dma.pack_ctrl(
            size = 2, # 0 = 8-bit, 1 = 16-bit, 2 = 32-bit
            inc_read = False,
            treq_sel = req_num,
            bswap = True
            # bswap = False # Test for OV5640
        )
        self.dma.config(
            read = self.sm,
            count = 244 * 324 // 4,
            # count = 240 * 320 * 2 // 4, # Test for OV5640
            ctrl = dma_ctrl
        )

    def active(self, active = None):
        if active == None:
            return self.sm.active()
        
        self.sm.active(active)

        if active:
            Pin(self.pin_vsync).irq(
                trigger = Pin.IRQ_FALLING,
                handler = lambda pin: self._vsync_handler()
            )
        else:
            Pin(self.pin_vsync).irq(
                handler = None
            )

    def _vsync_handler(self):
        # Disable DMA before reconfiguring it
        self.dma.active(False)

        # Reset state machine to ensure ISR is cleared
        self.sm.restart()

        # Ensure PIO RX FIFO is empty (it's not emptied by `sm.restart()`)
        while self.sm.rx_fifo() > 0:
            self.sm.get()

        # Reset the DMA write address
        self.dma.write = self.buffer

        # Start the DMA
        self.dma.active(True)

    @rp2.asm_pio(
            in_shiftdir = rp2.PIO.SHIFT_LEFT,
            push_thresh = 32,
            autopush = True,
            fifo_join = rp2.PIO.JOIN_RX
        )
    def _pio_read_dvp():
        wait(1, gpio, 0) # Mask in HSYNC pin
        wait(1, gpio, 0) # Mask in PCLK pin
        in_(pins, 1)     # Mask in number of pins
        wait(0, gpio, 0) # Mask in PCLK pin
