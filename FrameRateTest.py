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

camera = cv2.VideoCapture(0)
ball_im = cv2.imread("tests/maze_photo.png")

mazenodes = MazeNodes(ball_im)

fb = FindBall(mazenodes.start_lower, mazenodes.start_upper, mazenodes.filt_close, mazenodes.filt_open)

# Continually take image, find ball, print ball location, return time taken over all operations
while True:
    start_time = time.clock()
    retval, current_image = camera.read()
    ball_x, ball_y = fb.findBall(ball_im)
    print ball_x, ball_y
    print time.clock() - start_time
