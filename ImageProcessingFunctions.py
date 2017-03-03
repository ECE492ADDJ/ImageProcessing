"""
Filename:       ImageProcessingFunctions.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-21
Modified on:    2017-02-26
Description:    Utility functions for image processing.  Functions that are
                required by both MazeNodes.py and FindBall.py are saved here to
                avoid redundancy.
"""

import numpy as np
import cv2

def getImage(filename):
    # load the image
    image = cv2.imread(filename)

    return image

def drawResults(image, all_nodes, path_nodes):
    # Draw nodes
    for n in all_nodes:
        cv2.circle(image, n, 3, (150, 150, 150), -1)

    # cv2.circle(image, self.start.coordinates, 10, (0, 220, 220), -1)
    # cv2.circle(image, self.end.coordinates, 10, (200, 10, 200), -1)

    # Draw edges
    for n in all_nodes:
        if len(all_nodes.get(n).neighbours) > 4:
            print 'Too many neighbours!!'
        for nb in all_nodes.get(n).neighbours:
            cv2.line(image, n, nb.coordinates, (178, 178, 178), 2)
            # cv2.line(image, n, nb.coordinates, (nb.coordinates[0] % 255,
            #     nb.coordinates[1] % 255, (nb.coordinates[0] + nb.coordinates[1]) % 255), 2)

    # Draw path
    for n in range(0, len(path_nodes) - 1):
        cv2.line(image, path_nodes[n].coordinates, path_nodes[n + 1].coordinates, (255, 200, 0), 2)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)

    # cv2.imwrite("test_maze_noded.png", image)


def findRegionCenter(mask):
    # Use OpenCV to find the center of a colour region
    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, 2017-02-08
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    contours = cv2.findContours(thresh, 1, 2)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY

def findRegionCenterNeighbours(rc_node, nodes, x_div_len, y_div_len):
    """ Find neighbours to a node that does not necessarily fall on the grid (i.e.
        the start and end nodes) """
    x = rc_node.coordinates[0]
    y = rc_node.coordinates[1]
    rc_node.neighbours = []
    # Check for adjacent nodes in all directions
    for nx in range(x - x_div_len, x + x_div_len + 1):
        for ny in range(y - y_div_len, y + y_div_len + 1):
            if ((nx, ny) != (x, y)) and ((nx, ny) in nodes):
                rc_node.neighbours.append(nodes.get((nx, ny)))
                nodes.get((nx, ny)).neighbours.append(rc_node)
