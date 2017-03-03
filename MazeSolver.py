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

    image = getImage('paintmaze_small.png')

    # Run initial image processing
    mn = MazeNodes(image)
    mn.runProcessing()

    nodes = mn.nodes

    startNode = Node()
    endNode = Node()

    for n in nodes:
    	if nodes.get(n).start:
    		startNode = nodes.get(n)
    	if nodes.get(n).end:
    		endNode = nodes.get(n)

    findRegionCenterNeighbours(startNode, nodes, mn.x_div_len, mn.y_div_len)
    findRegionCenterNeighbours(endNode, nodes, mn.x_div_len, mn.y_div_len)

    pf = PathFinder(nodes, startNode, endNode)
    path = pf.findPath()

    directions = pf.translate(path)

    drawResults(image, nodes, path)

    trackImage = captureImage()
    fb = FindBall(mn.x_div_len, mn.y_div_len, mn.start_lower, mn.start_upper)

    while trackImage is not None:
        ball_x, ball_y = fb.findBall(trackImage)
        time.sleep(0.01) # small delay
        trackImage = captureImage()


if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    main()
