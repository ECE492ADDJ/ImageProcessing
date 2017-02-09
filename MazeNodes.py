# import the necessary packages
import numpy as np
import cv2
from Node import *
import sys

SIG_LENGTH = 10

NUM_DIVS_X = 30
NUM_DIVS_Y = 20

# define the list of colour ranges
WHITE_THRESHOLD =  ([240, 240, 240], [255, 255, 255])

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
    lower = np.array(WHITE_THRESHOLD[0], dtype = "uint8")
    upper = np.array(WHITE_THRESHOLD[1], dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # Convert mask output to greyscale
    # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
    gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    return image, gray_image, x_div_len, y_div_len

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
    image_name = sys.argv[1]
    main(image_name)
