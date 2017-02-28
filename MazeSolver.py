# import the necessary packages
import sys
from Node import *
from MazeNodes import MazeNodes
from PathFinder import PathFinder
from ImageProcessingFunctions import *


def main():

    image = getImage('paintmaze_small.png')

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

    drawResults(image, nodes, path)

if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    main()
 