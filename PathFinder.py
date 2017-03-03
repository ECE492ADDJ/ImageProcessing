"""
Filename:       PathFinder.py
File type:      server-side python code
Author:         Jacob Charlebois, Andrea McIntosh
Created on:     2017-02-10
Modified on:    2017-03-03
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

    def __init__(self, nodes, start, end):
        self.nodes = nodes
        self.startNode = start
        self.endNode = end

    def findPath(self):

        graph = {}

        for n in self.nodes:
            graph[self.nodes.get(n)] = self.nodes.get(n).neighbours

        path = self.shortestPath(graph, self.startNode, self.endNode)

        sp = self.reduceNodes(path)

        return path

    #http://code.activestate.com/recipes/576675-bfs-breadth-first-search-graph-traversal/
    def breadthFirstSearch(self, g, start):
        queue, enqueued = deque([(None, start)]), set([start])
        while queue:
            parent, n = queue.popleft()
            yield parent, n
            new = set(g[n]) - enqueued
            enqueued |= new
            queue.extend([(n, child) for child in new])

    def shortestPath(self, g, start, end):
        parents = {}
        for parent, child in self.breadthFirstSearch(g, start):
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

    def translate(self, path):
        """ Given an ordered list of nodes, translates the coordinates into directions """
        directions = []

        for p in range(len(path) - 1):
            x1 = path[p].coordinates[0]
            y1 = path[p].coordinates[1]
            x2 = path[p + 1].coordinates[0]
            y2 = path[p + 1].coordinates[1]

            diffx = x1 - x2
            diffy = y1 - y2

            if (diffx == 0 and diffy < 0):
                directions.append('Down')
            if (diffx == 0 and diffy > 0):
                directions.append('Up')
            if (diffx < 0 and diffy == 0):
                directions.append('Right')
            if (diffx > 0 and diffy == 0):
                directions.append('Left')

        return directions

    """ Remove redundant nodes (itermediate nodes in a straight line) from path """
    def reduceNodes(self, path):
        reduced_path = []
        p = 0
        reduced_path.append(path[p])

        while p < (len(path) - 1):
            if path[p].coordinates[0] == path[p + 1].coordinates[0]:
                while path[p].coordinates[0] == path[p + 1].coordinates[0]:
                    p += 1
                reduced_path.append(path[p])
            elif path[p].coordinates[1] == path[p + 1].coordinates[1]:
                while path[p].coordinates[1] == path[p + 1].coordinates[1]:
                    p += 1
                reduced_path.append(path[p])
            else:
                reduced_path.append(path[p])
            p += 1

        return reduced_path
