#!/usr/bin/python
from Node import *

class Dijkstras:
	'Find the shortest path between two nodes retrieved from image'

	def __init__(self, nodeList):
		'Requires only the full list of nodes. Will find the start and endpoint, then find a path between them.'
		self.unvisitedNodes = nodeList
		self.path = []
		print("Initialized")

	def findPoints(self):
		'Iterates through the list of nodes to find start and end points'
		for node in self.unvisitedNodes:
			if(node.start):
				self.startNode = node
			elif(node.end):
				self.endNode = node

	def startPath(self):
		'Starts recursive search through nodes'
		print("Starting Path!")
		self.unvisitedNodes.remove(self.startNode)
		currPath = [self.startNode]
		for node in self.startNode.neighbours:
			self.unvisitedNodes.remove(node)
			self.findPath(node, currPath)


	def findPath(self, currNode, currPath):
		'Recursively search through nodes looking for end point'
		print("Finding path!")
		print(len(currPath))
		currPath.append(currNode)
		if(currNode == self.endNode):
			print("At end!")
			self.path = currPath
			return
			
		for node in currNode.neighbours:
			if node in self.unvisitedNodes:

				self.unvisitedNodes.remove(node)
				self.findPath(node,currPath)

		# If the full path has not been found by in this branch, remove the branch from path
		if len(self.path) is 0:
				currPath.remove(currNode)
		




A = Node()
A.coordinates = (0,1)
A.start = True
print(A.coordinates)

B = Node()
B.end = False
B.coordinates = (0,2)

C = Node()
C.coordinates = (0,3)

D = Node()
D.coordinates = (0,4)

E = Node()
E.coordinates = (0,5)
E.end = False

F = Node()
F.end = True
F.coordinates = (0,6)

G = Node()
G.coordinates = (0,7)

A.neighbours.append(B)
A.neighbours.append(C)

C.neighbours.append(A)
C.neighbours.append(E)
C.neighbours.append(F)

F.neighbours.append(C)
F.neighbours.append(G)

G.neighbours.append(F)
G.neighbours.append(E)


E.neighbours.append(C)
E.neighbours.append(D)
E.neighbours.append(G)

D.neighbours.append(E)

B.neighbours.append(A)

path = Dijkstras([A,B,C,D,E,F,G]);
path.findPoints()
path.startPath()

print("Start and end points:")
print(path.startNode.coordinates);
print(path.endNode.coordinates);

print("neighbours of start:")
for element in A.neighbours:
	print(element.coordinates)

print("path:")	
for node in path.path:
	print(node.coordinates)