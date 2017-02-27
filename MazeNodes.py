"""
Filename:       MazeNodes.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-01-31
Modified on:    2017-02-26
Description:    Class that converts image of maze to a graph of nodes and edges
                for pathfinding.  Nodes are found by spliting the image into a
                grid and detecting colour regions.
"""

# import the necessary packages
import numpy as np
import cv2
from Node import *
from ImageProcessingFunctions import *

NUM_DIVS_X = 25
NUM_DIVS_Y = 25

# define the list of colour ranges
PLAY_THRESHOLD =  ([240, 240, 240], [255, 255, 255])
END_THRESHOLD =  ([0, 0, 150], [140, 140, 255])
START_THRESHOLD =  ([0, 150, 0], [160, 255, 160])


class MazeNodes:
    """ Take an image and convert it into nodes and edges for pathfinding """

    def __init__(self, image):
        self.image = image

        self.nodes = {}
        self.end = Node()
        self.start = Node()

        # http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
        # Create thresholds for colour detection
        self.end_lower = np.array(END_THRESHOLD[0], dtype = "uint8")
        self.end_upper = np.array(END_THRESHOLD[1], dtype = "uint8")
        self.start_lower = np.array(START_THRESHOLD[0], dtype = "uint8")
        self.start_upper = np.array(START_THRESHOLD[1], dtype = "uint8")
        self.play_lower = np.array(PLAY_THRESHOLD[0], dtype = "uint8")
        self.play_upper = np.array(PLAY_THRESHOLD[1], dtype = "uint8")

        # Find pixel length of each grid div
        self.x_div_len = int(len(image[0]) / NUM_DIVS_X) # floors number of divisions in width
        self.y_div_len = int(len(image) / NUM_DIVS_Y) # floors number of divisions in height


    def runProcessing(self):
        gray_image = self.preProcessImage()
        self.findNodes(gray_image)
        self.findEdges()
        drawResults(self.image, self.nodes, [])

    def preProcessImage(self):
        # Find endone and white it out
        # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
        end_mask = cv2.inRange(self.image, self.end_lower, self.end_upper) # find red area (endzone)
        self.findEnd(end_mask)
        self.image[np.where(end_mask == [255])] = 255 # white out endzone

        # Find start (ball) and white it out
        start_mask = cv2.inRange(self.image, self.start_lower, self.start_upper) # find green area (ball)
        self.findStart(start_mask)
        self.image[np.where(start_mask == [255])] = 255 # white out ball

        mask = cv2.inRange(self.image, self.play_lower, self.play_upper) # find white (playing) area
        self.image[np.where(mask == [255])] = 255 # white out white
        self.image[np.where(mask != [255])] = 0 # white out white

        # Convert mask output to greyscale
        # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        return gray_image

    def findStart(self, start_mask):
        # Find the start node (the ball) based on the mask generated by colour thresholds
        start_X, start_Y = findRegionCenter(start_mask)
        self.start.coordinates = (start_X, start_Y)
        self.start.neighbours = []
        self.start.start = True
        self.start.end = False
        self.nodes[self.start.coordinates] = self.start

    def findEnd(self, end_mask):
        # Find the end node based on the mask generated by colour thresholds
        end_X, end_Y = findRegionCenter(end_mask)
        self.end.coordinates = (end_X, end_Y)
        self.end.neighbours = []
        self.end.start = False
        self.end.end = True
        self.nodes[self.end.coordinates] = self.end

    def findNodes(self, gray_image):
        """ Find all valid nodes """
        # Run through all divisions
        for div_x in range(0, NUM_DIVS_X):
            for div_y in range(0, NUM_DIVS_Y):
                wall = False
                # Because image is a list of lists, need to run through the rows for each div
                for y_i in range(div_y*self.y_div_len, (div_y+1)*self.y_div_len):
                    if 0 in gray_image[y_i][div_x*self.x_div_len:(div_x+1)*self.x_div_len]:
                        wall = True
                # If the div does not contain any wall pixels, add to list of nodes for Dijksta's
                if not wall:
                    n = Node()
                    n.coordinates = (self.x_div_len*div_x+(self.x_div_len/2), self.y_div_len*div_y+(self.y_div_len/2))
                    n.neighbours = [] # need to make sure neighbours is empty
                    self.nodes[n.coordinates] = n

    def findEdges(self):
        """ Find all edges between nodes.  Edges only connect immediately adjacent
            nodes in straight (not diagonal) lines """
        for nc in self.nodes:
            x = nc[0]
            y = nc[1]
            nc_neighbours = self.nodes.get(nc).neighbours
            # Check for adjacent nodes in all directions
            if (x - self.x_div_len, y) in self.nodes:
                nc_neighbours.append(self.nodes.get((x - self.x_div_len, y)))
            if (x + self.x_div_len, y) in self.nodes:
                nc_neighbours.append(self.nodes.get((x + self.x_div_len, y)))
            if (x, y - self.y_div_len) in self.nodes:
                nc_neighbours.append(self.nodes.get((x, y - self.y_div_len)))
            if (x, y + self.y_div_len) in self.nodes:
                nc_neighbours.append(self.nodes.get((x, y + self.y_div_len)))
