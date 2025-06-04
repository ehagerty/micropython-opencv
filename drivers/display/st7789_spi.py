# Modified from:
# https://github.com/easytarget/st7789-framebuffer/blob/main/st7789_purefb.py

import struct
from time import sleep_ms
from ulab import numpy as np
import cv2

# ST7789 commands
_ST7789_SWRESET = b"\x01"
_ST7789_SLPIN = b"\x10"
_ST7789_SLPOUT = b"\x11"
_ST7789_NORON = b"\x13"
_ST7789_INVOFF = b"\x20"
_ST7789_INVON = b"\x21"
_ST7789_DISPOFF = b"\x28"
_ST7789_DISPON = b"\x29"
_ST7789_CASET = b"\x2a"
_ST7789_RASET = b"\x2b"
_ST7789_RAMWR = b"\x2c"
_ST7789_VSCRDEF = b"\x33"
_ST7789_COLMOD = b"\x3a"
_ST7789_MADCTL = b"\x36"
_ST7789_VSCSAD = b"\x37"
_ST7789_RAMCTL = b"\xb0"

# MADCTL bits
_ST7789_MADCTL_MY = const(0x80)
_ST7789_MADCTL_MX = const(0x40)
_ST7789_MADCTL_MV = const(0x20)
_ST7789_MADCTL_ML = const(0x10)
_ST7789_MADCTL_BGR = const(0x08)
_ST7789_MADCTL_MH = const(0x04)
_ST7789_MADCTL_RGB = const(0x00)

RGB = 0x00
BGR = 0x08

# 8 basic color definitions
BLACK = const(0x0000)
BLUE = const(0x001F)
RED = const(0xF800)
GREEN = const(0x07E0)
CYAN = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW = const(0xFFE0)
WHITE = const(0xFFFF)

_ENCODE_POS = const(">HH")

_BIT7 = const(0x80)
_BIT6 = const(0x40)
_BIT5 = const(0x20)
_BIT4 = const(0x10)
_BIT3 = const(0x08)
_BIT2 = const(0x04)
_BIT1 = const(0x02)
_BIT0 = const(0x01)

# Rotation tables
#   (madctl, width, height, xstart, ystart)[rotation % 4]

_DISPLAY_240x320 = (
    (0x00, 240, 320, 0, 0),
    (0x60, 320, 240, 0, 0),
    (0xc0, 240, 320, 0, 0),
    (0xa0, 320, 240, 0, 0))

_DISPLAY_170x320 = (
    (0x00, 170, 320, 35, 0),
    (0x60, 320, 170, 0, 35),
    (0xc0, 170, 320, 35, 0),
    (0xa0, 320, 170, 0, 35))

_DISPLAY_240x240 = (
    (0x00, 240, 240,  0,  0),
    (0x60, 240, 240,  0,  0),
    (0xc0, 240, 240,  0, 80),
    (0xa0, 240, 240, 80,  0))

_DISPLAY_135x240 = (
    (0x00, 135, 240, 52, 40),
    (0x60, 240, 135, 40, 53),
    (0xc0, 135, 240, 53, 40),
    (0xa0, 240, 135, 40, 52))

_DISPLAY_128x128 = (
    (0x00, 128, 128, 2, 1),
    (0x60, 128, 128, 1, 2),
    (0xc0, 128, 128, 2, 1),
    (0xa0, 128, 128, 1, 2))

# Supported displays (physical width, physical height, rotation table)
_SUPPORTED_DISPLAYS = (
    (240, 320, _DISPLAY_240x320),
    (170, 320, _DISPLAY_170x320),
    (240, 240, _DISPLAY_240x240),
    (135, 240, _DISPLAY_135x240),
    (128, 128, _DISPLAY_128x128))

# init tuple format (b'command', b'data', delay_ms)
_ST7789_INIT_CMDS = (
    ( b'\x11', b'\x00', 120),               # Exit sleep mode
    ( b'\x13', b'\x00', 0),                 # Turn on the display
    ( b'\xb6', b'\x0a\x82', 0),             # Set display function control
    ( b'\x3a', b'\x55', 10),                # Set pixel format to 16 bits per pixel (RGB565)
    ( b'\xb2', b'\x0c\x0c\x00\x33\x33', 0), # Set porch control
    ( b'\xb7', b'\x35', 0),                 # Set gate control
    ( b'\xbb', b'\x28', 0),                 # Set VCOMS setting
    ( b'\xc0', b'\x0c', 0),                 # Set power control 1
    ( b'\xc2', b'\x01\xff', 0),             # Set power control 2
    ( b'\xc3', b'\x10', 0),                 # Set power control 3
    ( b'\xc4', b'\x20', 0),                 # Set power control 4
    ( b'\xc6', b'\x0f', 0),                 # Set VCOM control 1
    ( b'\xd0', b'\xa4\xa1', 0),             # Set power control A
                                            # Set gamma curve positive polarity
    ( b'\xe0', b'\xd0\x00\x02\x07\x0a\x28\x32\x44\x42\x06\x0e\x12\x14\x17', 0),
                                            # Set gamma curve negative polarity
    ( b'\xe1', b'\xd0\x00\x02\x07\x0a\x28\x31\x54\x47\x0e\x1c\x17\x1b\x1e', 0),
    ( b'\x21', b'\x00', 0),                 # Enable display inversion
    ( b'\x29', b'\x00', 120)                # Turn on the display
)

class ST7789():
    """
    ST7789 driver class base
    """
    def __init__(self, width, height, backlight, bright, rotation, color_order, reverse_bytes_in_word):
        """
        Initialize display and backlight.
        """
        # Initial dimensions and offsets; will be overridden when rotation applied
        self.width = width
        self.height = height
        self.xstart = 0
        self.ystart = 0
        # backlight pin
        self.backlight = backlight
        self._pwm_bl = True
        # Check display is known and get rotation table
        self.rotations = self._find_rotations(width, height)
        if not self.rotations:
            supported_displays = ", ".join(
                [f"{display[0]}x{display[1]}" for display in _SUPPORTED_DISPLAYS])
            raise ValueError(
                f"Unsupported {width}x{height} display. Supported displays: {supported_displays}")
        # Colors
        self.color_order = color_order
        self.needs_swap = reverse_bytes_in_word
        # init the st7789
        self.init_cmds = _ST7789_INIT_CMDS
        self.soft_reset()
        # Yes, send init twice, once is not always enough
        self.send_init(self.init_cmds)
        self.send_init(self.init_cmds)
        # Initial rotation
        self._rotation = rotation % 4
        # Apply rotation
        self.rotation(self._rotation)
        # Create the framebuffer for the correct rotation
        self.buffer = np.zeros((self.rotations[self._rotation][2], self.rotations[self._rotation][1], 2), dtype=np.uint8)

    def send_init(self, commands):
        """
        Send initialisation commands to display.
        """
        for command, data, delay in commands:
            self._write(command, data)
            sleep_ms(delay)

    def soft_reset(self):
        """
        Soft reset display.
        """
        self._write(_ST7789_SWRESET)
        sleep_ms(150)

    def _find_rotations(self, width, height):
        """ Find the correct rotation for our display or return None """
        for display in _SUPPORTED_DISPLAYS:
            if display[0] == width and display[1] == height:
                return display[2]
        return None

    def rotation(self, rotation):
        """
        Set display rotation.

        Args:
            rotation (int):
                - 0-Portrait
                - 1-Landscape
                - 2-Inverted Portrait
                - 3-Inverted Landscape
        """
        if ((rotation % 2) != (self._rotation % 2)) and (self.width != self.height):
            # non-square displays can currently only be rotated by 180 degrees
            # TODO: can framebuffer of super class be destroyed and re-created
            #       to match the new dimensions? or it's width/height changed?
            return

        # find rotation parameters and send command
        rotation %= len(self.rotations)
        (   madctl,
            self.width,
            self.height,
            self.xstart,
            self.ystart, ) = self.rotations[rotation]
        if self.color_order == BGR:
            madctl |= _ST7789_MADCTL_BGR
        else:
            madctl &= ~_ST7789_MADCTL_BGR
        self._write(_ST7789_MADCTL, bytes([madctl]))
        # Set window for writing into
        self._write(_ST7789_CASET,
            struct.pack(_ENCODE_POS, self.xstart, self.width + self.xstart - 1))
        self._write(_ST7789_RASET,
            struct.pack(_ENCODE_POS, self.ystart, self.height + self.ystart - 1))
        self._write(_ST7789_RAMWR)
        # TODO: Can we swap (modify) framebuffer width/height in the super() class?
        self._rotation = rotation

    def imshow(self, image):
        """
        Display an image on the screen.

        Args:
            image (Image): Image to display
        """
        # Check if image is a NumPy ndarray
        if type(image) is not np.ndarray:
            raise TypeError("Image must be a NumPy ndarray")

        # Ensure image is 3D (row, col, ch) by reshaping if necessary
        ndim = len(image.shape)
        if ndim == 1:
            image = image.reshape((image.shape[0], 1, 1))
        elif ndim == 2:
            image = image.reshape((image.shape[0], image.shape[1], 1))

        # Determine number of rows, columns, and channels
        row, col, ch = image.shape

        # Crop input image to match display size
        row_max = min(row, self.height)
        col_max = min(col, self.width)
        img_cropped = image[:row_max, :col_max]

        # Crop the buffer if image is smaller than the display
        row_max = min(row_max, self.buffer.shape[0])
        col_max = min(col_max, self.buffer.shape[1])
        buffer_cropped = self.buffer[:row_max, :col_max]

        # Check dtype and convert to uint8 if necessary
        if img_cropped.dtype is not np.uint8:
            # Have to create a new buffer for non-uint8 images
            if img_cropped.dtype == np.int8:
                temp = cv2.convertScaleAbs(img_cropped, alpha=1, beta=127)
            elif img_cropped.dtype == np.int16:
                temp = cv2.convertScaleAbs(img_cropped, alpha=1/255, beta=127)
            elif img_cropped.dtype == np.uint16:
                temp = cv2.convertScaleAbs(img_cropped, alpha=1/255)
            elif img_cropped.dtype == np.float:
                # Standard OpenCV will clamp values to 0-1 using convertTo(),
                # but this implementation wraps instead
                temp = np.asarray(img_cropped * 255, dtype=np.uint8)
            img_cropped = temp

        # Convert image to BGR565 format
        if ch == 3:  # BGR
            buffer_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2BGR565, buffer_cropped)
        elif ch == 1:  # Grayscale
            buffer_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_GRAY2BGR565, buffer_cropped)
        else: # Already in BGR565 format
            buffer_cropped[:] = img_cropped

        # Write  to display. Swap bytes if needed
        if self.needs_swap:
            self._write(None, self.buffer[:, :, ::-1])
        else:
            self._write(None, self.buffer)

class ST7789_SPI(ST7789):
    """
    ST7789 driver class for SPI bus devices

    Args:
        spi (bus): bus object        **Required**
        width (int): display width   **Required**
        height (int): display height **Required**
        reset (pin): reset pin
        cs (pin): cs pin
        dc (pin): dc pin
        backlight (pin) or (pwm): backlight pin
          - can be type Pin (digital), PWM or None
        bright (value): Initial brightness level; default 'on'
          - a (float) between 0 and 1 if backlight is pwm
          - otherwise (bool) or (int) for pin value()
        rotation (int): Orientation of display
          - 0-Portrait, default
          - 1-Landscape
          - 2-Inverted Portrait
          - 3-Inverted Landscape
        color_order (int):
          - RGB: Red, Green Blue, default
          - BGR: Blue, Green, Red
        reverse_bytes_in_word (bool):
          - Enable if the display uses LSB byte order for color words
    """
    def __init__(
        self,
        spi,
        width,
        height,
        reset=None,
        cs=None,
        dc=None,
        backlight=None,
        bright=1,
        rotation=0,
        color_order=BGR,
        reverse_bytes_in_word=True,
    ):
        self.spi = spi
        self.reset = reset
        self.cs = cs
        self.dc = dc
        super().__init__(width, height, backlight, bright, rotation, color_order, reverse_bytes_in_word)

    def _write(self, command=None, data=None):
        """SPI write to the device: commands and data."""
        if self.cs:
            self.cs.off()
        if command is not None:
            self.dc.off()
            self.spi.write(command)
        if data is not None:
            self.dc.on()
            self.spi.write(data)
        if self.cs:
            self.cs.on()

    def hard_reset(self):
        """
        Hard reset display.
        """
        if self.cs:
            self.cs.off()
        if self.reset:
            self.reset.on()
        sleep_ms(10)
        if self.reset:
            self.reset.off()
        sleep_ms(10)
        if self.reset:
            self.reset.on()
        sleep_ms(120)
        if self.cs:
            self.cs.on()