# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

# load the image
image = cv2.imread("./paintmaze_small.jpg")

# define the list of colour ranges
boundaries =  [([240, 240, 240], [255, 255, 255])] # white

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # im2, contours, heiarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    im2, contours, heiarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print contour
    cv2.drawContours(image, contours, -1, (255, 0, 0), 3)

    # # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)
