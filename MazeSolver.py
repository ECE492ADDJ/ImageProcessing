#pylint: disable=E1101

"""
Filename:       MazeSolver.py
File type:      server-side python code
Author:         Jake Charlebois, Andrea McIntosh
Created on:     2017-02-27
Modified on:    2017-03-02
Description:    Main control script for python server
"""

# import the necessary packages
import sys
import time
import getopt
from collections import deque
import cv2
import ImageProcessingFunctions as img
from MazeNodes import MazeNodes
from PathFinder import PathFinder
from FindBall import FindBall
from BallPathPlanner import BallPathPlanner
from ServoController import ServoConnection
from SerialException import SerialException

# TODO: Allow these values to be changed at runtime.
MAX_ACC = 100
FRAMERATE = 15
ACC_MULTIPLIER = 1
SER_COUNT = 20

class MazeSolver(object):
    """
    Top level class for maze solving. Responsible for high level coordination of other classes.

    play_colour_upper: Defines the upper colour threshold for the play space. This value should be
    a list of three integers of the format [B, G, R].

    play_colour_lower: Defines the lower colour threshold for the play space. This value should be
    a list of three integers of the format [B, G, R].

    start_colour_upper: Defines the upper colour threshold for the start (ball). This value should
    be a list of three integers of the format [B, G, R].

    start_colour_lower: Defines the lower colour threshold for the start (ball). This value should
    be a list of three integers of the format [B, G, R].

    end_colour_upper: Defines the upper colour threshold for the end of the maze. This value should
    be a list of three integers of the format [B, G, R].

    end_colour_lower: Defines the lower colour threshold for the end of the maze. This value should
    be a list of three integers of the format [B, G, R].

    serial_port: The serial port that should be used to connect to the DE2.

    camera_index: The index of the camera to be used in monitoring the maze.

    update_callback: A function to be called every time the MazeSolver updates after run() has been
    called. This callback can be expected to be called approximately 30 times per second. This
    callback should be a function that takes in a single argument that is a MazeSolver object.

    fixed_image_path: A debug attribute to set a fixed image to be solved. This attribute should be
    set to the path of the image. If this attribute is set, the camera will not be used and only
    the inital image processing will be run.
    """

    def __init__(self):
        self.play_colour_upper = [255, 255, 255]
        self.play_colour_lower = [200, 200, 200]
        self.start_colour_upper = [160, 255, 160]
        self.start_colour_lower = [0, 175, 0]
        self.end_colour_upper = [140, 140, 255]
        self.end_colour_lower = [0, 0, 150]

        self.serial_port = '/dev/ttyUSB0'
        self.camera_index = 0
        self.fixed_image_path = None
        self.debug = False

        self.update_callback = lambda ms: None

        self._current_image = None
        self._path = None
        self._finished = True
        self._stopped = False
        self._ball_x = 0
        self._ball_y = 0
        self._end_x = 0
        self._end_y = 0
        self._target_coords = (0, 0)
        self._acc_x = 0
        self._acc_y = 0
        self._ser_results = deque(maxlen=SER_COUNT)

    def run(self):
        """
        Starts the maze solving process. This method blocks until the maze has been solved, but
        will call update_callback on a regular basis to allow the UI to be updated.
        """
        self._stopped = False
        self._finished = False

        if self.fixed_image_path is None:
            camera = cv2.VideoCapture(self.camera_index)
            retval, self._current_image = camera.read()

            if not retval:
                raise IOError("Failed to read initial image from camera.")
        else:
            self._current_image = cv2.imread(self.fixed_image_path)

        # Run initial image processing
        mazenodes = MazeNodes(self._current_image, self.end_colour_lower, self.end_colour_upper,
                                self.start_colour_lower, self.start_colour_upper,
                                  self.play_colour_lower, self.play_colour_upper, self.debug)
        mazenodes.runProcessing()

        nodes = mazenodes.nodes
        start_node = mazenodes.start
        end_node = mazenodes.end

        # Start and end nodes not necessarily on grid with other nodes, must find
        #  their neighbours separately
        img.findRegionCenterNeighbours(start_node, nodes, mazenodes.x_div_len, mazenodes.y_div_len)
        img.findRegionCenterNeighbours(end_node, nodes, mazenodes.x_div_len, mazenodes.y_div_len)

        # Find path through maze
        pathfinder = PathFinder(nodes, start_node, end_node)
        self._path = pathfinder.findPath()

        self._end_x, self._end_y = end_node.coordinates

        if self.debug:
            img.drawResults(self._current_image, nodes, self._path, start_node, end_node)

        if not self.fixed_image_path is None:
            # Debug: draw result of pathfinding
            img.drawResults(self._current_image, nodes, self._path, start_node, end_node)
        else:
            # Live ball tracking
            ball_finder = FindBall(mazenodes.start_lower, mazenodes.start_upper,
                    mazenodes.filt_close, mazenodes.filt_open)
            planner = BallPathPlanner(self._path)

            with ServoConnection(port=self.serial_port) as conn:
                try:
                    flat_x = conn.get_x_val()
                    flat_y = conn.get_y_val()
                except SerialException:
                    flat_x = conn.get_x_val()
                    flat_y = conn.get_y_val()

                while not planner.isFinished():
                    if self._stopped:
                        break

                    start_time = time.clock()
                    retval, self._current_image = camera.read()
                    if not retval:
                        raise IOError("Failed to read image from camera.")

                    self._ball_x, self._ball_y = ball_finder.findBall(self._current_image)
                    self._acc_x, self._acc_y = planner.getAcceleration(self._ball_x, self._ball_y)
                    self._target_coords = planner.get_target_pos()

                    try:
                        new_x_acc = max(-1 * MAX_ACC, min(MAX_ACC, self._acc_x * ACC_MULTIPLIER + flat_x))
                        new_y_acc = max(-1 * MAX_ACC, min(MAX_ACC, self._acc_y * ACC_MULTIPLIER + flat_y))
                        conn.set_x_val(int(new_x_acc))
                        self._ser_results.append(1)
                        time.sleep(0.001)
                        conn.set_y_val(int(new_y_acc))
                        self._ser_results.append(1)
                    except SerialException as ex:
                        print ex
                        self._ser_results.append(0)

                    self.update_callback(self)

                    time.sleep(max(1.0 / FRAMERATE - (time.clock() - start_time), 0))

                self._finished = planner.isFinished()

            # TODO: Release camera under all circumstances
            camera.release()

    def is_finished(self):
        """
        Returns a boolean value indicating whether the maze has been solved or not. If run() has
        not been called, this method will return False.
        """
        return self._finished

    def get_ball_pos(self):
        """
        Returns a tuple containing the (X, Y) values of the current ball position.
        """
        return (self._ball_x, self._ball_y)

    def get_end_pos(self):
        """
        Returns a tuple containing the (X, Y) values of the end node.
        """
        return (self._end_x, self._end_y)

    def get_target_pos(self):
        """
        Returns a tuple containing the (X, Y) values of the current target position.
        """
        return self._target_coords

    def get_acceleration(self):
        """
        Returns a tuple representing the current acceleration.
        """
        return (self._acc_x, self._acc_y)

    def get_image(self):
        """
        Returns the most recent image.
        """
        return self._current_image

    def get_serial_success_rate(self):
        """
        Gets the fraction of recent serial operations that have succeeded expressed as a number
        between 0 and 1.
        """
        return float(reduce(lambda x, y: x + y, self._ser_results)) / len(self._ser_results)

    def get_path(self):
        """
        Returns a list of node objects that represent the ball path.
        """
        return self._path

    def stop(self):
        """
        Stops the maze solver.
        """
        self._stopped = True

def parseThreshold(threshold):
    """
    Parses a threshold expressed as a string in the format "B,G,R" (no spaces). Returns a list in
    the format [B, G, R] where B, G, and R are integers.
    """
    strings = threshold.split(",")
    return [int(string) for string in strings]

if __name__ == '__main__':
    try:
        options, remains = getopt.getopt(sys.argv[1:], "",
                ["help=", "image=", "camera=", "serial=", "play_upper=", "play_lower=",
                "start_upper=", "start_lower=", "end_upper=", "end_lower=", "debug"])
    except getopt.GetoptError:
        print "usage: MazeSolver.py [--help] [--image <image file>] [--camera <index>] \
[--serial <port name>] [--play_upper B,G,R] [--play_lower B,G,R] [--start_upper B,G,R] \
[--start_lower B,G,R] [--end_upper B,G,R] [--end_lower B,G,R]"
        sys.exit(1)

    solver = MazeSolver()

    for option, value in options:
        if option == "--help":
            print "usage: MazeSolver.py [--help] [--image <image file>] [--camera <index>] \
[--serial <port name>] [--play_upper B,G,R] [--play_lower B,G,R] [--start_upper B,G,R] \
[--start_lower B,G,R] [--end_upper B,G,R] [--end_lower B,G,R]"
            sys.exit(0)
        elif option == "--image":
            solver.fixed_image_path = value
        elif option == "--camera":
            solver.camera_index = int(value)
        elif option == "--serial":
            solver.serial_port = value
        elif option == "--play_upper":
            solver.play_colour_upper = parseThreshold(value)
        elif option == "--play_lower":
            solver.play_colour_lower = parseThreshold(value)
        elif option == "--start_upper":
            solver.start_colour_upper = parseThreshold(value)
        elif option == "--start_lower":
            solver.start_colour_lower = parseThreshold(value)
        elif option == "--end_upper":
            solver.end_colour_upper = parseThreshold(value)
        elif option == "--end_lower":
            solver.end_colour_lower = parseThreshold(value)
        elif option == "--debug":
            solver.debug = True

    solver.run()
