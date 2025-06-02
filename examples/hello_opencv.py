# Import OpenCV, just as you would in any other Python environment!
import cv2

# Import NumPy. Note that we use ulab's NumPy, which is a lightweight version of
# standard NumPy
from ulab import numpy as np

# Import a display driver. Any display driver can be used, as long as it
# implements an `imshow()` function that takes an NumPy array as input
import st7789_spi as st7789

# The display driver requires some hardware-specific imports
from machine import Pin, SPI

# Create SPI object
spi = SPI(0, baudrate=24000000)

# Create display object
display = st7789.ST7789_SPI(spi,
                            240, 320,
                            reset=None,
                            cs=machine.Pin(17, Pin.OUT, value=1),
                            dc=machine.Pin(16, Pin.OUT, value=1),
                            backlight=None,
                            bright=1,
                            rotation=1,
                            color_order=st7789.BGR,
                            reverse_bytes_in_word=True)

# Initialize an image (NumPy array) to be displayed
img = np.zeros((240,320, 3), dtype=np.uint8)

# Images can be modified directly if desired. Here we set the top 50 rows of the
# image to blue (255, 0, 0) in BGR format
img[0:50, :] = (255, 0, 0)

# OpenCV's drawing functions can be used to modify the image as well. For
# example, we can draw a green ellipse on the image. Note that many OpenCV
# functions return the output image, meaning the entire array will be printed
# if it's not assigned to a variable. In this case, we assign the output to the
# same variable `img`, which has almost no overhead
img = cv2.ellipse(img, (160, 120), (100, 50), 0, 0, 360, (0, 255, 0), -1)

# And the obligatory text, this time in red
img = cv2.putText(img, "Hello OpenCV!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Once we have an image ready to show, just call `imshow()` as you would in
# any other Python environment! However it's a bit different here, as we
# don't have a window to show the image in. Instead, we pass the display object
# to the `imshow()` function, which will show the image on the screen
cv2.imshow(display, img)
