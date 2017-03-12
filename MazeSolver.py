"""
Filename:       MazeSolver.py
File type:      server-side python code
Author:         Jake Charlebois, Andrea McIntosh
Created on:     2017-02-27
Modified on:    2017-03-02
Description:    Main control script for python server
"""

# import the necessary packages
import sys
from Node import *
from MazeNodes import MazeNodes
from PathFinder import PathFinder
from FindBall import FindBall
from ImageProcessingFunctions import *
from ConnectToCamera import captureImage

import time

def main():
    # A static test image for un-integrated testing.  Will be replaced by an image
    #  from the USB camera in the future
    image = getImage('tests/maze_photo_4.png')

    # Run initial image processing
    mn = MazeNodes(image)
    mn.runProcessing()

    nodes = mn.nodes

    # Test: draw results of image processing (nodes and edges found)
    drawResults(image, nodes, [], mn.start, mn.end)

    startNode = mn.start
    endNode = mn.end

    # Start and end nodes not necessarily on grid with other nodes, must find
    #  their neighbours separately
    findRegionCenterNeighbours(startNode, nodes, mn.x_div_len, mn.y_div_len)
    findRegionCenterNeighbours(endNode, nodes, mn.x_div_len, mn.y_div_len)

    # Find path through maze
    pf = PathFinder(nodes, startNode, endNode)
    path = pf.findPath()
    directions = pf.translate(path)

    # Test: draw result of pathfinding
    drawResults(image, nodes, path, startNode, endNode)

    # Live ball tracking
    trackImage = captureImage()
    fb = FindBall(mn.x_div_len, mn.y_div_len, mn.start_lower, mn.start_upper)

    while trackImage is not None:
        ball_x, ball_y = fb.findBall(trackImage)
        time.sleep(0.01) # small delay
        trackImage = captureImage()


if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    main()
