#-------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
# 
# Copyright (c) 2025 SparkFun Electronics
#-------------------------------------------------------------------------------
# ex01_touch_drive.py
# 
# This example creates a simple touch screen interface to drive the XRP robot.
# It creates arrow buttons to drive around, and a stop button to exit the
# example. The XRP is available from SparkFun:
# https://www.sparkfun.com/experiential-robotics-platform-xrp-kit.html
#-------------------------------------------------------------------------------

# Import XRPLib defaults
from XRPLib.defaults import *

# Import OpenCV and hardware initialization module
import cv2 as cv
from cv2_hardware_init import *

# Import NumPy
from ulab import numpy as np

# Initialize arrow button image
btn_arrow_shape = (50, 50, 3)
btn_arrow_cx = btn_arrow_shape[1] // 2
btn_arrow_cy = btn_arrow_shape[0] // 2
btn_arrow_length = 30
btn_arrow_thickness = 5
btn_arrow_tip_length = 0.5
btn_arrow_offset = 75
img_btn_arrow_vertical = np.zeros(btn_arrow_shape, dtype=np.uint8)
img_btn_arrow_vertical[:, :] = (255, 0, 0)
img_btn_arrow_horizontal = img_btn_arrow_vertical.copy()
img_btn_arrow_vertical = cv.arrowedLine(
    img_btn_arrow_vertical,
    (btn_arrow_cx, btn_arrow_cy + btn_arrow_length // 2),
    (btn_arrow_cx, btn_arrow_cy - btn_arrow_length // 2),
    (255, 255, 255),
    btn_arrow_thickness,
    cv.FILLED,
    0,
    btn_arrow_tip_length
)
img_btn_arrow_horizontal = cv.arrowedLine(
    img_btn_arrow_horizontal,
    (btn_arrow_cx - btn_arrow_length // 2, btn_arrow_cy),
    (btn_arrow_cx + btn_arrow_length // 2, btn_arrow_cy),
    (255, 255, 255),
    btn_arrow_thickness,
    cv.FILLED,
    0,
    btn_arrow_tip_length
)

# Initialize stop button image
btn_stop_shape = (50, 50, 3)
btn_stop_cx = btn_stop_shape[1] // 2
btn_stop_cy = btn_stop_shape[0] // 2
btn_stop_size = 25
img_btn_stop = np.zeros(btn_stop_shape, dtype=np.uint8)
img_btn_stop[:, :] = (0, 0, 255)  # Red color
img_btn_stop = cv.rectangle(
    img_btn_stop,
    (btn_stop_cx - btn_stop_size // 2, btn_stop_cy - btn_stop_size // 2),
    (btn_stop_cx + btn_stop_size // 2, btn_stop_cy + btn_stop_size // 2),
    (255, 255, 255),  # White border
    -1  # Fill the rectangle
)

# Initialize UI image
ui_img = np.zeros((240, 320, 3), dtype=np.uint8)
# Draw the stop button in the center
center_x = ui_img.shape[1] // 2
center_y = ui_img.shape[0] // 2
ui_img[
    center_y-btn_stop_cy:center_y+btn_stop_cy,
    center_x-btn_stop_cx:center_x+btn_stop_cx
] = img_btn_stop
# Draw the forward arrow above the stop button
ui_img[
    center_y-btn_arrow_offset-btn_arrow_cy:center_y-btn_arrow_offset+btn_arrow_cy,
    center_x-btn_arrow_cx:center_x+btn_arrow_cx
] = img_btn_arrow_vertical
# Draw the backward arrow below the stop button
ui_img[
    center_y+btn_arrow_offset-btn_arrow_cy:center_y+btn_arrow_offset+btn_arrow_cy,
    center_x-btn_arrow_cx:center_x+btn_arrow_cx
] = img_btn_arrow_vertical[::-1, :, :]  # Flip the arrow image vertically
# Draw the right arrow to the right of the stop button
ui_img[
    center_y-btn_arrow_cy:center_y+btn_arrow_cy,
    center_x+btn_arrow_offset-btn_arrow_cx:center_x+btn_arrow_offset+btn_arrow_cx
] = img_btn_arrow_horizontal
# Draw the left arrow to the left of the stop button
ui_img[
    center_y-btn_arrow_cy:center_y+btn_arrow_cy,
    center_x-btn_arrow_offset-btn_arrow_cx:center_x-btn_arrow_offset+btn_arrow_cx
] = img_btn_arrow_horizontal[:, ::-1, :]  # Flip the arrow image horizontally

# Show the UI image on the display
cv.imshow(display, ui_img)

# Prompt the user to touch the screen to drive around
print("Touch the screen to drive around. Press any key to exit.")

# Loop to continuously read touch input and drive around
while True:
    # Read touch input
    x, y, touch_num = touch_screen.get_touch()

    if touch_num > 0:
        # Check if the stop button was pressed
        if (center_x - btn_stop_cx <= x <= center_x + btn_stop_cx and
            center_y - btn_stop_cy <= y <= center_y + btn_stop_cy):
            print("Stop")
            break
        # Check if the forward arrow was pressed
        elif (center_x - btn_arrow_cx <= x <= center_x + btn_arrow_cx and
              center_y - btn_arrow_offset - btn_arrow_cy <= y <= center_y - btn_arrow_offset + btn_arrow_cy):
            print("Forward")
            drivetrain.straight(20, 0.5)
        # Check if the backward arrow was pressed
        elif (center_x - btn_arrow_cx <= x <= center_x + btn_arrow_cx and
              center_y + btn_arrow_offset - btn_arrow_cy <= y <= center_y + btn_arrow_offset + btn_arrow_cy):
            print("Backward")
            drivetrain.straight(-20, 0.5)
        # Check if the right arrow was pressed
        elif (center_y - btn_arrow_cy <= y <= center_y + btn_arrow_cy and
              center_x + btn_arrow_offset - btn_arrow_cx <= x <= center_x + btn_arrow_offset + btn_arrow_cx):
            print("Right")
            drivetrain.turn(-90, 0.5)
        # Check if the left arrow was pressed
        elif (center_y - btn_arrow_cy <= y <= center_y + btn_arrow_cy and
              center_x - btn_arrow_offset - btn_arrow_cx <= x <= center_x - btn_arrow_offset + btn_arrow_cx):
            print("Left")
            drivetrain.turn(90, 0.5)

    if cv.waitKey(1) != -1:
        # Exit the loop if any key is pressed
        break

# Clear the display
display.clear()
