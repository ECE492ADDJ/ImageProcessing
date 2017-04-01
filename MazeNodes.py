#pylint: disable=E1101

"""
Filename:       MazeNodes.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-01-31
Modified on:    2017-02-26
Description:    Class that converts image of maze to a graph of nodes and edges
                for pathfinding.  Nodes are found by spliting the image into a
                grid and detecting colour regions.
                Tested by printing out results using ImageProcessingFunctions.drawResults()

>>> image = cv2.imread("tests/MazeNodes_pytest_small_maze.png")
>>> mn = MazeNodes(image)
>>> g_img = mn.preProcessImage()
>>> mn.x_div_count
4
>>> mn.y_div_count
5
>>> mn.x_div_len
125
>>> mn.y_div_len
50
>>> mn.start.coordinates
(75, 125)
>>> mn.end.coordinates
(425, 125)
>>> mn.findNodes(g_img)
>>> len(mn.nodes)
8
"""

# import the necessary packages
import numpy as np
import cv2
from Node import *
from ImageProcessingFunctions import *

class MazeNodes:
    """
    Take an image and convert it into nodes and edges for pathfinding
    """

    def __init__(self, image, end_thresh_low = [160, 80, 230], end_thresh_high = [180, 100, 255],
                                start_thresh_low = [0, 90, 100], start_thresh_high = [50, 220, 220],
                                  play_thresh_low = [40, 40, 40], play_thresh_high = [255, 255, 255]):
        self.image = image

        self.nodes = {}
        self.end = Node()
        self.start = Node()

        self.end_lower = end_thresh_low
        self.end_upper = end_thresh_high
        self.start_lower = start_thresh_low
        self.start_upper = start_thresh_high
        self.play_lower = play_thresh_low
        self.play_upper = play_thresh_high

        # rayryeng, http://stackoverflow.com/questions/30369031/remove-spurious-small-islands-of-noise-in-an-image-python-opencv, 2017-03-16
        self.filt_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        self.filt_open = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))

        self.x_div_len = None
        self.y_div_len = None

        self.x_div_count = None
        self.y_div_count = None

        self.min_path_thickness = 30
        self.scan_interval = 20
        self.nodes_per_path = 2


    def runProcessing(self):
        """
        Run all steps needed for image processing
        """
        gray_image = self.preProcessImage()
        self.findNodes(gray_image)
        self.findEdges()

    def preProcessImage(self):
        """
        Prepare image for subsequent image processing.  Modifies original image
        object and also returns a grayscale version of the image
        """
        # http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
        # Create thresholds for colour detection
        end_lower_np = np.array(self.end_lower, dtype="uint8")
        end_upper_np = np.array(self.end_upper, dtype="uint8")
        start_lower_np = np.array(self.start_lower, dtype="uint8")
        start_upper_np = np.array(self.start_upper, dtype="uint8")
        play_lower_np = np.array(self.play_lower, dtype="uint8")
        play_upper_np = np.array(self.play_upper, dtype="uint8")

        # Find endone and white it out
        # http://answers.opencv.org/question/97416/replace-a-range-of-colors-with-a-specific-color-in-python/, 2017-02-08
        end_mask = cv2.inRange(self.image, end_lower_np, end_upper_np) # find endzone area
        self.findEnd(end_mask)
        self.image[np.where(end_mask == [255])] = 255 # white out endzone

        cv2.imshow("End Mask", end_mask)
        cv2.waitKey(0)

        # Find start (ball) and white it out
        start_mask = cv2.inRange(self.image, start_lower_np, start_upper_np) # find ball (start)
        self.findStart(start_mask)
        self.image[np.where(start_mask == [255])] = 255 # white out ball

        cv2.imshow("Start Mask", start_mask)
        cv2.waitKey(0)

        mask = cv2.inRange(self.image, play_lower_np, play_upper_np) # find white (playing) area
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.filt_close)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.filt_open)
        self.image[np.where(mask == [255])] = 255 # white out white
        self.image[np.where(mask != [255])] = 0 # white out white

        cv2.imshow("Play Mask", mask)
        cv2.waitKey(0)

        # Determine the grid size based on path thickness
        path_width, path_height = self._getPathThickness(mask)
        self.x_div_count = int(len(self.image[0]) / (path_width / (self.nodes_per_path + 1)))
        self.y_div_count = int(len(self.image) / (path_height / (self.nodes_per_path + 1)))
        self.x_div_len = int(len(self.image[0]) / self.x_div_count)
        self.y_div_len = int(len(self.image) / self.y_div_count)

        # Convert mask output to greyscale
        # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        return gray_image

    def findStart(self, start_mask):
        """
        Find the start node (the ball) based on the mask generated by colour thresholds
        """
        try:
            start_X, start_Y = findRegionCenter(start_mask, self.filt_open, self.filt_close)
        except:
            raise ValueError("Image has no start colour region")
        self.start.coordinates = (start_X, start_Y)
        self.start.neighbours = []
        self.start.start = True
        self.start.end = False
        self.nodes[self.start.coordinates] = self.start

    def findEnd(self, end_mask):
        """
        Find the end node based on the mask generated by colour thresholds
        """
        try:
            end_X, end_Y = findRegionCenter(end_mask, self.filt_open, self.filt_close)
        except:
            raise ValueError("Image has no end colour region")
        self.end.coordinates = (end_X, end_Y)
        self.end.neighbours = []
        self.end.start = False
        self.end.end = True
        self.nodes[self.end.coordinates] = self.end

    def findNodes(self, gray_image):
        """
        Find all valid nodes in a grayscale image
        """
        if self.x_div_count is None or self.y_div_count is None:
            raise RuntimeError("Image preprocessing has not been run.")

        # Run through all divisions
        for div_x in range(0, self.x_div_count):
            for div_y in range(0, self.y_div_count):
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
        """
        Find all edges between nodes.  Edges only connect immediately adjacent
            nodes in straight (not diagonal) lines
        """
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

    #Naive and slow implementation
    def _getPathThickness(self, mask):
        """
        Determines the path thickness by scanning row by row and column by column. The minimum
        thickness of play space (as determined by the mask) in each direction is used. Any paths
        found that are narrower than min_path_thickness are ignored. To improve speed, scanning is
        done at a given interval of scan_interval.

        mask: The mask of the play space. It is assumed that 0 represents non play area and 255
        represents play area.

        NOTE: This code assumes that the mask of the maze will only feature walls oriented at 90
        degrees from each other and that these walls will be aligned with the rows and columns of
        the image.
        """
        width = float("inf")
        height = float("inf")

        # Rows
        for i in range(0, mask.shape[0], self.scan_interval):
            temp = self._getShortestSequence(mask[i])
            if temp > self.min_path_thickness:
                width = min(width, temp)

        # Columns
        for j in range(0, mask.shape[1], self.scan_interval):
            temp = self._getShortestSequence(mask[:, j])
            if temp > self.min_path_thickness:
                height = min(height, temp)

        if width == float("inf"):
            raise ValueError("No valid path width found. The scan interval may be too high.")

        if height == float("inf"):
            raise ValueError("No valid path height found. The scan interval may be too high.")

        return (width, height)

    def _getShortestSequence(self, pixels):
        """
        Finds the length of the shortest sequence of play space pixels in a line of pixels. A play
        space pixel is assumed to have a value of 255 while a non play space pixel is assumed to
        have a value of 0. Returns float("inf") if no play space pixels are found.

        pixels: An iterable object containing the pixel values.
        """
        count = 0
        mincount = float("inf")
        prevpixel = 0

        for pixel in pixels:
            if pixel == 0 and prevpixel != 0:
                if count >= self.min_path_thickness:
                    mincount = min(count, mincount)
                count = 0
            elif pixel == 255:
                count += 1

            prevpixel = pixel

        if prevpixel != 0:
            if count >= self.min_path_thickness:
                mincount = min(count, mincount)

        return mincount

# For running doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
