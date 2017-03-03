"""
Filename:       FindBall.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-03-02
Description:    Use video frames to continuously detect the location of the ball
"""

import numpy as np
import cv2, time
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

        ball_history.append(((ball_x, ball_y), time.clock())) # save position and time found at

        print ball_x, ball_y
        return ball_x, ball_y

    def calcAcceleration(self):
        len_hist = len(self.ball_history)
        if len_hist > 3:
            vel_1_x, vel_1_y = self.calcVelocity(self.ball_history[len_hist - 3], self.ball_history[len_hist - 2])
            vel_2_x, vel_2_y = self.calcVelocity(self.ball_history[len_hist - 2], self.ball_history[len_hist - 1])

            acc_x = (vel_2_x - vel_1_x) / (self.ball_history[len_hist - 1][1] - self.ball_history[len_hist - 3][1])
            acc_y = (vel_2_y - vel_1_y) / (self.ball_history[len_hist - 1][1] - self.ball_history[len_hist - 3][1])
            return

    # expects postions as tuples of ((x, y), time)
    def calcVelocity(self, start_pos, curr_pos):
        # velocities in pixels/sec
        vel_x = (curr_pos[0][0] - start_pos[0][0]) / (curr_pos[1] - start_pos[1])
        vel_y = (curr_pos[0][1] - start_pos[0][1]) / (curr_pos[1] - start_pos[1])
        return vel_x, vel_y
