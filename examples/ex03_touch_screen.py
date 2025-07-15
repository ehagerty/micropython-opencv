#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2025 SparkFun Electronics
#-------------------------------------------------------------------------------
# ex03_touch_screen.py
# 
# This example demonstrates how to read input from a touch screen, which can be
# used to verify that the touch screen driver is functioning. It simply draws
# lines on a blank image based on touch input, similar to a drawing application.
#-------------------------------------------------------------------------------

# Import OpenCV and hardware initialization module
import cv2 as cv
from cv2_hardware_init import *

# Import NumPy
from ulab import numpy as np

# Initialize an image to draw on
img = np.zeros((240, 320, 3), dtype=np.uint8)

# Prompt the user to draw on the screen
img = cv.putText(img, "Touch to draw!", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Prompt the user to press a key to continue
print("Press any key to continue")

# Create variables to store touch coordinates and state
x0, y0, x1, y1 = 0, 0, 0, 0
touching = False

# Loop to continuously read touch input and draw on the image
while True:
    # Read touch input
    x, y, touch_num = touch_screen.get_touch()

    # Update the touch coordinates and state
    if touch_num > 0:
        if not touching:
            x0 = x
            y0 = y
            x1 = x
            y1 = y
            touching = True
        else:
            x0 = x1
            y0 = y1
            x1 = x
            y1 = y
    else:
        if touching:
            touching = False

    # Draw a line if touching
    if touching:
        img = cv.line(img, (x0, y0), (x1, y1), (255, 255, 255), 2)

    # Display the frame
    display.imshow(img)

    # Check for key presses
    key = cv.waitKey(1)

    # If any key is pressed, exit the loop
    if key != -1:
        break
