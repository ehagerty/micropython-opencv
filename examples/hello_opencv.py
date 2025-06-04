# Import OpenCV, just as you would in any other Python environment!
import cv2

# Import NumPy. Note that we use ulab's NumPy, which is a lightweight version of
# standard NumPy
from ulab import numpy as np

# Import a display driver. Any display driver can be used, as long as it
# implements an `imshow()` function that takes an NumPy array as input
import st7789_spi as st7789

# Create display object
display = st7789.ST7789_SPI(width=240,
                            height=320,
                            spi_id=0,
                            pin_cs=17,
                            pin_dc=16,
                            rotation=1,)

# Initialize an image (NumPy array) to be displayed
img = np.zeros((240, 320, 3), dtype=np.uint8)

# Images can be modified directly if desired. Here we set the top 50 rows of the
# image to blue (255, 0, 0) in BGR format
img[0:50, :] = (255, 0, 0)

# OpenCV's drawing functions can be used to modify the image as well. For
# example, we can draw a green ellipse on the image. Note that many OpenCV
# functions return the output image, meaning the entire array will be printed
# if it's not assigned to a variable. In this case, we assign the output to the
# same variable `img`, which has almost no overhead
img = cv2.ellipse(img, (160, 120), (100, 50), 0, 0, 360, (0, 255, 0), -1)

# And the obligatory "Hello OpenCV" text, this time in red
img = cv2.putText(img, "Hello OpenCV!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Once we have an image ready to show, just call `imshow()` as you would in
# any other Python environment! However it's a bit different here, as we
# don't have a window to show the image in. Instead, we pass the display object
# to the `imshow()` function, which will show the image on the screen
cv2.imshow(display, img)
