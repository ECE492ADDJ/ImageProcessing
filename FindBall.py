"""
Filename:       FindBall.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-03-02
Description:    Use video frames to continuously detect the location of the ball
"""

import numpy as np
import cv2
from ImageProcessingFunctions import *
from MazeNodes import NUM_DIVS_X, NUM_DIVS_Y, START_THRESHOLD

class FindBall:

    def __init__(self, x_div_len, y_div_len, start_lower, start_upper):
        # Get variables calcualted in MazeNodes
        self.x_div_len = x_div_len
        self.y_div_len = y_div_len
        self.thresh_lower = start_lower
        self.thresh_upper = start_upper

        self.ball_history = []

    def findBall(self, image):
        # Find ball:
        # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
        ball_mask = cv2.inRange(image, self.thresh_lower, self.thresh_upper) # find ball
        ball_x, ball_y = findRegionCenter(ball_mask)

        self.ball_history.append((ball_x, ball_y))

        print ball_x, ball_y

    def calcAcceleration():
        if len(self.ball_history) > 3:
            return
