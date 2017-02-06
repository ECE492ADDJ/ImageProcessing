# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

SIG_LENGTH = 10

NUM_DIVS = 32

# load the image
image = cv2.imread("./paintmaze_small.jpg")

# define the list of colour ranges
boundaries =  [([240, 240, 240], [255, 255, 255])] # white

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # Convert mask output to greyscale
    # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
    gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    nodes = []
    x_div = int(len(gray_image[0]) / NUM_DIVS) # floors number of divisions in width
    y_div = int(len(gray_image) / NUM_DIVS) # floors number of divisions in height
    # Run through all divisions
    for div_x in range(0, NUM_DIVS):
        for div_y in range(0, NUM_DIVS):
            wall = False
            # Because image is a list of lists, need to run through the rows for each div
            for y_i in range(div_y*y_div, (div_y+1)*y_div):
                if 0 in gray_image[y_i][div_x*x_div:(div_x+1)*x_div]:
                    wall = True
            # If the div does not contain any wall pixels, add to list of nodes for Dijksta's
            if not wall:
                nodes.append((x_div*div_x+(div_x/2), y_div*div_y+(div_y/2)))

    for n in nodes:
        cv2.circle(image, n, 5, (255, 255, 0), -1)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)

    # cv2.imwrite("maze_points.png", image)
