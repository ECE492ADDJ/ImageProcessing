#!/usr/bin/python
class Node:
	'Node object which will contain information about intersections in the maze. Each node will maintain whether it is a start or end point, coordinates, and a list of neighbouring nodes.'

	# def __init__(self):
	start = False
	end = False
	coordinates = ()
	neighbours = []
