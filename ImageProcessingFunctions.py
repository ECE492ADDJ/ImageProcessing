"""
Filename:       ImageProcessingFunctions.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-02-26
Description:    Utility functions for image processing.  Functions that are
                required by multiple modules are saved here to avoid redundancy.

>>> im = cv2.imread('tests/ball_location_test.png')
>>> len(im)
250
>>> len(im[0])
250
>>> ball_mask = cv2.inRange(im, (0, 0, 0), (255, 50, 0))
>>> findRegionCenter(ball_mask)
(125, 125)
>>> from Node import Node
>>> n1 = Node()
>>> n1.coordinates = (0,0)
>>> n1.neighbours = []
>>> n2 = Node()
>>> n2.coordinates = (10,10)
>>> n2.neighbours = []
>>> rc = Node()
>>> rc.coordinates = (1,2)
>>> rc.neighbours = []
>>> nodes = {(0,0): n1, (1,2): rc, (10,10): n2}
>>> findRegionCenterNeighbours(rc, nodes, 4, 3)
>>> len(rc.neighbours)
1
>>> rc.neighbours[0] == n1
True
"""

import numpy as np
import cv2

def getImage(filename):
    """
    Load an image from a filename (used for testing functions before connecting to
    actual camera)

    Input: filename (and path if not in current directory) of image to load
    Output: image
    """
    image = cv2.imread(filename)

    return image

def drawResults(image, all_nodes, path_nodes, start, end):
    """
    Draw any features (nodes, start, end, edges, path) calculated by image processing
    on the original image.  Good for testing image processing, thresholds, and
    number of divisions.

    Input: original image, list of all Node objects found, ordered list of all Node
        objects in path found, start Node object, end Node object
    """

    # Draw edges
    for n in all_nodes:
        for nb in all_nodes.get(n).neighbours:
            cv2.line(image, n, nb.coordinates, (128, 200, 128), 2)

    # Draw nodes
    for n in all_nodes:
        cv2.circle(image, n, 2, (100, 100, 100), -1)

    # Draw start and end
    cv2.circle(image, start.coordinates, 10, (255, 150, 50), -1)
    cv2.circle(image, end.coordinates, 10, (10, 10, 255), -1)

    # Draw path
    for n in range(0, len(path_nodes) - 1):
        cv2.circle(image, path_nodes[n].coordinates, 5, (0, 255, 0), -1)
        cv2.line(image, path_nodes[n].coordinates, path_nodes[n + 1].coordinates, (0, 255, 0), 2)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)


def findRegionCenter(mask, filt_close, filt_open):
    """
    Use OpenCV to find the center of a colour region.  Includes filtering the
    input mask to reduce noise.

    Input: mask showing the location of the colour region
           filt_close: OpenCV structuring element to filter noise by performing
                a dilation then erosion (closing)
           filt_close: OpenCV structuring element to filter noise by performing
                an erosion then dilation (opening)
    """
    # Filter mask to reduce noise
    # rayryeng, http://stackoverflow.com/questions/30369031/remove-spurious-small-islands-of-noise-in-an-image-python-opencv, 2017-03-16
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, filt_close)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, filt_open)

    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, 2017-02-08
    # ret, thresh = cv2.threshold(mask, 127, 255, 0)
    contours = cv2.findContours(mask, 1, 2)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY

def findRegionCenterNeighbours(rc_node, nodes, x_div_len, y_div_len):
    """
    Find neighbours to a node that does not necessarily fall on the grid (i.e.
        the start and end nodes)

    Input: Node object that neighbours should be determined for, list of all nodes
        in graph, length of an x-axis division, length of a y-axis division
    """
    x = rc_node.coordinates[0]
    y = rc_node.coordinates[1]
    rc_node.neighbours = []
    # Check for adjacent nodes in all directions
    for nx in range(x - x_div_len, x + x_div_len + 1):
        for ny in range(y - y_div_len, y + y_div_len + 1):
            # Neightbour should be within one division length in any direction
            if ((nx, ny) != (x, y)) and ((nx, ny) in nodes):
                rc_node.neighbours.append(nodes.get((nx, ny)))
                nodes.get((nx, ny)).neighbours.append(rc_node)

# For running doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
