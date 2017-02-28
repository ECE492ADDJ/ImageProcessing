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

    def __init__(self, nodes, start, end):
        self.nodes = nodes
        self.startNode = start
        self.endNode = end

    def findPath(self):

        graph = {}

        for n in self.nodes:
            graph[self.nodes.get(n)] = self.nodes.get(n).neighbours
        
        path = self.shortestPath(graph, self.startNode, self.endNode)

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
