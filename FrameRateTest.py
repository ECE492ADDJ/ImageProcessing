"""
Filename:       FrameRateTest.py
File type:      test code
Author:         Andrea McIntosh
Created on:     2017-03-20
Modified on:    2017-03-20
Description:    Function to test camera frame rate when finding ball for each frame.
"""

from FindBall import FindBall
from MazeNodes import MazeNodes
import numpy as np
import cv2, time

# Open a camera object to record latency of capturing images, but use a test image
#   to actually find ball position.  This way the frame rate can be tested even
#   when not connected to the actual project.
camera = cv2.VideoCapture(0)
ball_im = cv2.imread("tests/maze_photo.png")

mazenodes = MazeNodes(ball_im)

fb = FindBall(mazenodes.start_lower, mazenodes.start_upper, mazenodes.filt_close, mazenodes.filt_open)

# Save the delays of each trial
rates = []

# Take image, find ball, return time taken over all operations
# Perform test 100 times
x = 0
while x < 100:
    start_time = time.clock()
    retval, current_image = camera.read()
    ball_x, ball_y = fb.findBall(ball_im)
    t = time.clock() - start_time
    rates.append(t)
    x += 1

# Find average delay over all trials
s = 0
for r in rates:
    s += r
print s/len(rates)
