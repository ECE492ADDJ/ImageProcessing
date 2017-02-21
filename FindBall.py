import numpy as np
import cv2
from ImageProcessingFunctions import *

GREEN_THRESHOLD =  ([0, 150, 0], [160, 255, 160])

def getImage(filename):
    # load the image
    image = cv2.imread(filename)

    # http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
    # create NumPy arrays from the boundaries
    green_lower = np.array(GREEN_THRESHOLD[0], dtype = "uint8")
    green_upper = np.array(GREEN_THRESHOLD[1], dtype = "uint8")

    # Find ball and endzone:
    # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
    start_mask = cv2.inRange(image, green_lower, green_upper) # find green area (ball)
    start_X, start_Y = findRegionCenter(start_mask)

    return image, gray_image, x_div_len, y_div_len
