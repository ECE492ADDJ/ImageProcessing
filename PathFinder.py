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

Testing for BFS algorithm
>>> graph = {'A':['B', 'C'], 'B':['A', 'D'], 'D':['B', 'H'], 'H':['D', 'J'], 'J':['H'], 'C':['A', 'E'], 'E':['C', 'F', 'G'], 'F':['E'], 'G':['E']}
>>> pf1 = PathFinder(graph, 'A', 'J')
>>> pf1.shortestPath(graph, 'A', 'J')
['A', 'B', 'D', 'H', 'J']
>>> pf2 = PathFinder(graph, 'J', 'G')
>>> pf2.shortestPath(graph, 'J', 'G')
['J', 'H', 'D', 'B', 'A', 'C', 'E', 'G']
>>> pf3 = PathFinder(graph, 'F', 'G')
>>> pf3.shortestPath(graph, 'F', 'G')
['F', 'E', 'G']

Testing for translation
>>> A = Node()
>>> B = Node()
>>> C = Node()
>>> D = Node()
>>> E = Node()
>>> A.neighbours = [B, C]
>>> B.neighbours = [A]
>>> C.neighbours = [A, D]
>>> D.neighbours = [C, E]
>>> E.neighbours = [D]
>>> A.coordinates = (1, 1)
>>> B.coordinates = (2, 1)
>>> C.coordinates = (1, 2)
>>> D.coordinates = (1, 3)
>>> E.coordinates = (2, 3)
>>> nodes = {(1, 1):A, (2, 1):B, (1, 2):C, (1, 3):D, (2, 3):E}
>>> pf4 = PathFinder(nodes, B, E)
>>> path = pf4.findPath()
>>> pf4.translate(path)
['Left', 'Down', 'Down', 'Right']

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
        """ Find a path from the start of the graph to the end """
        graph = {}

        for n in self.nodes:
            graph[self.nodes.get(n)] = self.nodes.get(n).neighbours

        path = self.shortestPath(graph, self.startNode, self.endNode)

        return self.reduceNodes(path)

    #http://code.activestate.com/recipes/576675-bfs-breadth-first-search-graph-traversal/
    def breadthFirstSearch(self, g, start):
        """ Implementation of the breadth first search pathfinding algorithm """
        queue, enqueued = deque([(None, start)]), set([start])
        while queue:
            parent, n = queue.popleft()
            yield parent, n
            new = set(g[n]) - enqueued
            enqueued |= new
            queue.extend([(n, child) for child in new])

    def shortestPath(self, g, start, end):
        """ Run breadthFirstSearch and return the path as a list of nodes in the correct order """
        parents = {}
        for parent, child in self.breadthFirstSearch(g, start):
            parents[child] = parent
            if child == end:
                # Once path is found, reverse the order of the nodes in the path list
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

    def reduceNodes(self, path):
        """ Remove redundant nodes (itermediate nodes in a straight line) from path """
        reduced_path = []
        p = 0
        reduced_path.append(path[p])

        # For Nodes in a straight line (either same x coordinates or same y coordinates)
        #   only keep first and last Node in the line in the list of path Nodes
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
