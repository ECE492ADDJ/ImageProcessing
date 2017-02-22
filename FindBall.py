import numpy as np
import cv2, sys
from ImageProcessingFunctions import *
from MazeNodes import NUM_DIVS_X, NUM_DIVS_Y

GREEN_THRESHOLD =  ([0, 150, 0], [160, 255, 160])

def findBall(filename):
    # load the image
    image = cv2.imread(filename)
    # Find pixel length of each grid div
    x_div_len = int(len(image[0]) / NUM_DIVS_X) # floors number of divisions in width
    y_div_len = int(len(image) / NUM_DIVS_Y) # floors number of divisions in height

    # http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
    # create NumPy arrays from the boundaries
    green_lower = np.array(GREEN_THRESHOLD[0], dtype = "uint8")
    green_upper = np.array(GREEN_THRESHOLD[1], dtype = "uint8")

    # Find ball and endzone:
    # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
    ball_mask = cv2.inRange(image, green_lower, green_upper) # find green area (ball)
    ball_X, ball_Y = findRegionCenter(ball_mask)

    ball.coordinates = (ball_X, ball_Y)
    ball.neighbours = []
    ball.start = True
    ball.end = False
    image[np.where(ball_mask == [255])] = 255 # white out green ball
    nodes[ball.coordinates] = ball

    print ball_X, ball_Y

if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    image_name = sys.argv[1]
    findBall(image_name)
