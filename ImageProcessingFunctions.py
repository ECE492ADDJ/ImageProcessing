import numpy as np
import cv2

def findRegionCenter(mask):
    # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html, 2017-02-08
    ret,thresh = cv2.threshold(mask,127,255,0)
    contours = cv2.findContours(thresh, 1, 2)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY

def findRegionCenterNeighbours(rc_node, nodes, x_div_len, y_div_len):
    x = rc_node.coordinates[0]
    y = rc_node.coordinates[1]
    rc_node.neighbours = []
    # Check for adjacent nodes in all directions
    for nx in range(x - x_div_len, x + x_div_len + 1):
        for ny in range(y - y_div_len, y + y_div_len + 1):
            if ((nx, ny) != (x, y)) and ((nx, ny) in nodes):
                rc_node.neighbours.append(nodes.get((nx, ny)))
