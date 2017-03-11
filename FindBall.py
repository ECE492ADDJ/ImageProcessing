"""
Filename:       FindBall.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-03-02
Description:    Use video frames to continuously detect the location of the ball

>>> fb = FindBall(5, 5, (0, 0, 0), (255, 255, 255))
>>> fb.ball_history = [((1,1), 0), ((2,1), 1), ((4,1), 2)]
>>> len(fb.ball_history)
3
>>> fb.calcAcceleration()
(0.5, 0.0)
>>> fb.ball_history = [((1,1), 0), ((2,3), 1), ((3,9), 2)]
>>> fb.calcAcceleration()
(0.0, 2.0)
>>> fb.ball_history = [((1,1), 0), ((2,3), 1), ((5,9), 2), ((11,18), 3)]
>>> fb.calcAcceleration()
(1.5, 1.5)
>>> image = cv2.imread('ball_location_test.png')
>>> fb.findBall(image)
(124, 124)
"""

import numpy as np
import cv2, time
from ImageProcessingFunctions import *
#from MazeNodes import NUM_DIVS_X, NUM_DIVS_Y, START_THRESHOLD

class FindBall:

    def __init__(self, x_div_len, y_div_len, start_lower, start_upper):
        # Get variables calcualted in MazeNodes
        self.x_div_len = x_div_len
        self.y_div_len = y_div_len
        self.thresh_lower = start_lower
        self.thresh_upper = start_upper

        self.ball_history = []

    def findBall(self, image):
        """
        Determine current location of ball (center pixel location) in an image of the maze
        """
        # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
        ball_mask = cv2.inRange(image, self.thresh_lower, self.thresh_upper) # find ball
        ball_x, ball_y = findRegionCenter(ball_mask)

        self.ball_history.append(((ball_x, ball_y), time.clock())) # save position and time found at

        return ball_x, ball_y

    def calcAcceleration(self):
        """
        Based on previous 3 ball positions, determine current acceleration of the ball
        """
        len_hist = len(self.ball_history)
        if len_hist >= 3:
            vel_1_x, vel_1_y = self.calcVelocity(self.ball_history[len_hist - 3], self.ball_history[len_hist - 2])
            vel_2_x, vel_2_y = self.calcVelocity(self.ball_history[len_hist - 2], self.ball_history[len_hist - 1])

            acc_x = float(vel_2_x - vel_1_x) / (self.ball_history[len_hist - 1][1] - self.ball_history[len_hist - 3][1])
            acc_y = float(vel_2_y - vel_1_y) / (self.ball_history[len_hist - 1][1] - self.ball_history[len_hist - 3][1])
            return acc_x, acc_y
        return None

    def calcVelocity(self, start_pos, curr_pos):
        """
        Based on previous two positions, determine current velocity of the ball

        Input: expects postions as tuples of position coordinates and time at that position: ((x, y), time)
        Output: velocities in pixels/sec
        """
        vel_x = (curr_pos[0][0] - start_pos[0][0]) / (curr_pos[1] - start_pos[1])
        vel_y = (curr_pos[0][1] - start_pos[0][1]) / (curr_pos[1] - start_pos[1])
        return vel_x, vel_y

# For running doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
