"""
Filename:       PathFinder.py
File type:      server-side python code
Author:         Jacob Charlebois
Created on:     2017-02-10
Modified on:    2017-02-28
Description:    Class that finds the shortest path between a start and end node
                and stores it as an ordered list of nodes needed to be traversed
                in order to solve a maze. It relies on the MazeNodes class to handle
                the image processing of converting an image to a dict of nodes.
"""

# necessary packages
from Node import *
from MazeNodes import MazeNodes
from ImageProcessingFunctions import *
from collections import deque

class PathFinder:
    """ Finds a path for any given graph generated via image processing """

def main():
    image = getImage('paintmaze_small.png')

    mn = MazeNodes(image)
    mn.runProcessing()

    nodes = mn.nodes

    startNode = Node()
    endNode = Node()

    for j in nodes:
	if nodes.get(j).start:
		startNode = nodes.get(j)
	if nodes.get(j).end:
		endNode = nodes.get(j)

    findRegionCenterNeighbours(startNode, nodes, mn.x_div_len, mn.y_div_len)
    findRegionCenterNeighbours(endNode, nodes, mn.x_div_len, mn.y_div_len)

    graph = {}

    for n in nodes:
        graph[nodes.get(n)] = nodes.get(n).neighbours
    
    path = shortestPath(graph, startNode, endNode)
 
    drawResults(image, nodes, path)


#http://code.activestate.com/recipes/576675-bfs-breadth-first-search-graph-traversal/
def breadthFirstSearch(g, start):
    queue, enqueued = deque([(None, start)]), set([start])
    while queue:
        parent, n = queue.popleft()
        yield parent, n
        new = set(g[n]) - enqueued
        enqueued |= new
        queue.extend([(n, child) for child in new])

def shortestPath(g, start, end):
    parents = {}
    for parent, child in breadthFirstSearch(g, start):
        parents[child] = parent
        if child == end:
            revpath = [end]
            while True:
                parent = parents[child]
                revpath.append(parent)
                if parent == start:
                    break
                child = parent
            return list(reversed(revpath))
    return None # or raise appropriate exception

# 	return path

if __name__ == '__main__':
    # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2017-02-08
    main()
