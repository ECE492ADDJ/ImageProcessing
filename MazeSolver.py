# import the necessary packages
import sys
from Node import *
import Dijkstras
import MazeNodes
from ImageProcessingFunctions import *


def main(fn):
    image, gray_image, x_div_len, y_div_len = MazeNodes.getImage(fn)
    MazeNodes.findNodes(gray_image, x_div_len, y_div_len)
    MazeNodes.findEdges(x_div_len, y_div_len)
    nodes = MazeNodes.nodes

    startNode = Node()
    endNode = Node()

    for j in nodes:
        if nodes.get(j).start:
            startNode = nodes.get(j)
        if nodes.get(j).end:
            endNode = nodes.get(j)

    findRegionCenterNeighbours(startNode, nodes, x_div_len, y_div_len)
    findRegionCenterNeighbours(endNode, nodes, x_div_len, y_div_len)
    #Perform Dijkstras



    MazeNodes.drawResults(image, nodes)

if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    image_name = sys.argv[1]
    main(image_name)
 