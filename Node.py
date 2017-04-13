#!/usr/bin/python
"""
Filename:       Node.py
Author:			David Ross, Jake Charlebois
File type:      python class
Created on:     2017-02-06
Description:    Class defining Node objects that make up maze graph

Node class tests
>>> A = Node()
>>> A.neighbours = [1, 2, 3]
>>> A.start = True
>>> A.coordinates = (2, 2)
>>> A.neighbours
[1, 2, 3]
>>> A.start
True
>>> A.coordinates
(2, 2)
"""

class Node:
	'Node object which will contain information about intersections in the maze. Each node will maintain whether it is a start or end point, coordinates, and a list of neighbouring nodes.'

	# def __init__(self):
	start = False
	end = False
	coordinates = ()
	neighbours = []
