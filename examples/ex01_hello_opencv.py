# Import OpenCV, just as you would in any other Python environment!
import cv2

# Import NumPy, almost like any other Python environment! The only difference is
# the addition of `from ulab` since MicroPython does not have a full NumPy
# implementation; ulab NumPy is a lightweight version of standard NumPy
from ulab import numpy as np

# Standard OpenCV leverages the host operating system to display images, but we
# don't have that luxury in MicroPython. Instead, we need to import a display
# driver. Any display driver can be used, as long as it implements an `imshow()`
# method that takes an NumPy array as input
from st7789_spi import ST7789_SPI

# Create a display object. This will depend on the display driver you are using,
# and you may need to adjust the parameters based on your specific display and
# board configuration
display = ST7789_SPI(width=240,
                    height=320,
                    spi_id=0,
                    pin_cs=17,
                    pin_dc=16,
                    rotation=1)

# Initialize an image (NumPy array) to be displayed, just like in any other
# Python environment! Here we create a 240x320 pixel image with 3 color channels
# (BGR order, like standard OpenCV) and a data type of `uint8` (you should
# always specify the data type, because NumPy defaults to `float`)
img = np.zeros((240, 320, 3), dtype=np.uint8)

# Images can be accessed and modified directly if desired with array slicing.
# Here we set the top 50 rows of the image to blue (remember, BGR order!)
img[0:50, :] = (255, 0, 0)

# OpenCV's drawing functions can be used to modify the image as well. For
# example, we can draw a green ellipse at the center of the image
img = cv2.ellipse(img, (160, 120), (100, 50), 0, 0, 360, (0, 255, 0), -1)

# Note - Most OpenCV functions return the resulting image. It's redundant for
# the drawing functions and often ignored, but if you call those functions from
# the REPL without assigning it to a variable, the entire array will be printed.
# To avoid this, you can simply re-assign the image, which has no effect other
# than preventing the output from being printed

# And the obligatory "Hello OpenCV" text! This time in red
img = cv2.putText(img, "Hello OpenCV!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Once we have an image ready to show, just call `cv2.imshow()`, almost like any
# other Python environment! The only difference is that we need to pass the
# display object we created earlier as the first argument, instead of a window
# name string. Alternatively, you can call `display.imshow(img)` directly
cv2.imshow(display, img)

# Standard OpenCV requires a call to `cv2.waitKey()` to process events and
# actually display the image. However the display driver shows the image
# immediately, so it's not necessary to call `cv2.waitKey()` in MicroPython.
# But it is available, and behaves almost like any other Python environment! The
# only difference is that it requires a key to be pressed in the REPL instead of
# a window. It will wait for up to the specified number of milliseconds (0 for
# indefinite), and return the ASCII code of the key pressed (-1 if no key press)
# 
# Note - Some MicroPython IDEs (like Thonny) don't actually send any key presses
# until you hit Enter on your keyboard
key = cv2.waitKey(1) # Not necessary to display image, can remove if desired
