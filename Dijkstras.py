#!/usr/bin/python
import sys
from Node import *
from MazeNodes import MazeNodes
from ImageProcessingFunctions import *
from collections import deque

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

    # # Creating a fully undirected graph. Hardcoded madness, we will have to change how we find regioncenterneighbours
    # for n in nodes:
    # 	if n == (47, 25):
    # 		nodes.get(n).neighbours.append(startNode)
    #
    # 	if n == (66, 25):
    # 		nodes.get(n).neighbours.append(startNode)
    #
    # 	if n == (47, 42):
    # 		nodes.get(n).neighbours.append(startNode)
    #
    # 	if n == (66, 42):
    # 		nodes.get(n).neighbours.append(startNode)
    #
    # 	if n == (503, 25):
    # 		nodes.get(n).neighbours.append(endNode)
    #
    # 	if n == (522, 25):
    # 		nodes.get(n).neighbours.append(endNode)
    #
    graph = {}

    for n in nodes:
        graph[nodes.get(n)] = nodes.get(n).neighbours
    #
    path = shortest_path(graph, startNode, endNode)
    #
    # printnode = {}
    # for elem in path:
    #     printnode[elem.coordinates] = elem

    drawResults(image, nodes, path)


#http://code.activestate.com/recipes/576675-bfs-breadth-first-search-graph-traversal/
def bfs(g, start):
    queue, enqueued = deque([(None, start)]), set([start])
    while queue:
        parent, n = queue.popleft()
        yield parent, n
        new = set(g[n]) - enqueued
        enqueued |= new
        queue.extend([(n, child) for child in new])

def shortest_path(g, start, end):
    parents = {}
    for parent, child in bfs(g, start):
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
    # image_name = sys.argv[1]
    main()
