# import the necessary packages
import numpy as np
import cv2
from Node import *
import sys

NUM_DIVS_X = 30
NUM_DIVS_Y = 20

# define the list of colour ranges
WHITE_THRESHOLD =  ([240, 240, 240], [255, 255, 255])
RED_THRESHOLD =  ([0, 0, 150], [140, 140, 255])
GREEN_THRESHOLD =  ([0, 150, 0], [160, 255, 160])

nodes = {}

def main(fn):
    image, gray_image, x_div_len, y_div_len = getImage(fn)
    findNodes(gray_image, x_div_len, y_div_len)
    findEdges(x_div_len, y_div_len)
    drawResults(image)

def getImage(filename):
    # load the image
    image = cv2.imread(filename)

    # Find pixel length of each grid div
    x_div_len = int(len(image[0]) / NUM_DIVS_X) # floors number of divisions in width
    y_div_len = int(len(image) / NUM_DIVS_Y) # floors number of divisions in height

    # http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
    # create NumPy arrays from the boundaries
    red_lower = np.array(RED_THRESHOLD[0], dtype = "uint8")
    red_upper = np.array(RED_THRESHOLD[1], dtype = "uint8")
    green_lower = np.array(GREEN_THRESHOLD[0], dtype = "uint8")
    green_upper = np.array(GREEN_THRESHOLD[1], dtype = "uint8")
    white_lower = np.array(WHITE_THRESHOLD[0], dtype = "uint8")
    white_upper = np.array(WHITE_THRESHOLD[1], dtype = "uint8")

    end_mask = cv2.inRange(image, red_lower, red_upper) # find red area (endzone)
    # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
    end_X, end_Y = findRegionCenter(end_mask)
    image[np.where(end_mask == [255])] = 255 # white out red endzone

    ball_mask = cv2.inRange(image, green_lower, green_upper) # find green area (ball)
    ball_X, ball_Y = findRegionCenter(ball_mask)
    image[np.where(ball_mask == [255])] = 255 # white out green ball

    mask = cv2.inRange(image, white_lower, white_upper) # find white (playing) area
    image[np.where(mask == [255])] = 255 # white out green ball

    # Convert mask output to greyscale
    # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image, gray_image, x_div_len, y_div_len

def findRegionCenter(mask):
    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, 2017-02-08
    ret,thresh = cv2.threshold(mask,127,255,0)
    contours = cv2.findContours(thresh, 1, 2)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(mask, (cX, cY), 10, (200, 0, 255), -1)

    return cX, cY

def findNodes(gray_image, x_div_len, y_div_len):
    # Run through all divisions
    for div_x in range(0, NUM_DIVS_X):
        for div_y in range(0, NUM_DIVS_Y):
            wall = False
            # Because image is a list of lists, need to run through the rows for each div
            for y_i in range(div_y*y_div_len, (div_y+1)*y_div_len):
                if 0 in gray_image[y_i][div_x*x_div_len:(div_x+1)*x_div_len]:
                    wall = True
            # If the div does not contain any wall pixels, add to list of nodes for Dijksta's
            if not wall:
                n = Node()
                n.coordinates = (x_div_len*div_x+(x_div_len/2), y_div_len*div_y+(y_div_len/2))
                n.neighbours = [] # need to make sure neighbours is empty
                nodes[n.coordinates] = n

def findEdges(x_div_len, y_div_len):
    # Create edges
    for nc in nodes:
        x = nc[0]
        y = nc[1]
        nc_neighbours = nodes.get(nc).neighbours

        # Check for adjacent nodes in all directions
        if (x - x_div_len, y) in nodes:
            nc_neighbours.append(nodes.get((x - x_div_len, y)))

        if (x + x_div_len, y) in nodes:
            nc_neighbours.append(nodes.get((x + x_div_len, y)))

        if (x, y - y_div_len) in nodes:
            nc_neighbours.append(nodes.get((x, y - y_div_len)))

        if (x, y + y_div_len) in nodes:
            nc_neighbours.append(nodes.get((x, y + y_div_len)))

def drawResults(image):
    # Draw nodes
    for n in nodes:
        cv2.circle(image, n, 5, (150, 150, 150), -1)

    # Draw edges
    for n in nodes:
        if len(nodes.get(n).neighbours) > 4:
            print 'Too many neighbours!!'
        for nb in nodes.get(n).neighbours:
            cv2.line(image, n, nb.coordinates, (nb.coordinates[0] % 255,
                nb.coordinates[1] % 255, (nb.coordinates[0] + nb.coordinates[1]) % 255), 3)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)

if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    image_name = sys.argv[1]
    main(image_name)
