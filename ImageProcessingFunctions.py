"""
Filename:       ImageProcessingFunctions.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-02-26
Description:    Utility functions for image processing.  Functions that are
                required by multiple modules are saved here to avoid redundancy.
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
    # Draw nodes
    for n in all_nodes:
        cv2.circle(image, n, 3, (150, 150, 150), -1)

    # Draw start and end
    cv2.circle(image, start.coordinates, 10, (0, 220, 220), -1)
    cv2.circle(image, end.coordinates, 10, (200, 10, 200), -1)

    # Draw edges
    for n in all_nodes:
        for nb in all_nodes.get(n).neighbours:
            cv2.line(image, n, nb.coordinates, (178, 178, 178), 2)

    # Draw path
    for n in range(0, len(path_nodes) - 1):
        cv2.circle(image, path_nodes[n].coordinates, 10, (0, 0, 255), -1)
        cv2.line(image, path_nodes[n].coordinates, path_nodes[n + 1].coordinates, (255, 200, 0), 2)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)


def findRegionCenter(mask):
    """
    Use OpenCV to find the center of a colour region.

    Input: mask showing the location of the colour region
    """
    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, 2017-02-08
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    contours = cv2.findContours(thresh, 1, 2)

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
