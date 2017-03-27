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
import cv2
import getopt
import ImageProcessingFunctions as img
from MazeNodes import MazeNodes
from PathFinder import PathFinder
from FindBall import FindBall
from BallPathPlanner import BallPathPlanner
from ServoController import ServoConnection
from SerialException import SerialException

# TODO: Allow these values to be changed at runtime.
MAX_ACC = 150
FRAMERATE = 5
ACC_MULTIPLIER = 5

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
        self.camera_index = 1
        self.fixed_image_path = None

        self.update_callback = lambda ms: None

        self._current_image = None
        self._play_mask = None
        self._start_mask = None
        self._end_mask = None
        self._path = None
        self._finished = True

    def run(self):
        """
        Starts the maze solving process. This method blocks until the maze has been solved, but
        will call update_callback on a regular basis to allow the UI to be updated.
        """
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
                                  self.play_colour_lower, self.play_colour_upper)
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

        if not self.fixed_image_path is None:
            # Debug: draw result of pathfinding
            img.drawResults(self._current_image, nodes, self._path, start_node, end_node)
        else:
            # Live ball tracking
            ball_finder = FindBall(mazenodes.start_lower, mazenodes.start_upper,
                    mazenodes.filt_close, mazenodes.filt_open)
            planner = BallPathPlanner(self._path)
            # TODO: Allow planner speed, latency, acceleration factor, etc to be set a runtime.
            # Possibly through a config file?
            planner.speed = 1
            planner.latency = 0

            with ServoConnection(port=self.serial_port) as conn:
                flat_x = conn.get_x_val()
                flat_y = conn.get_y_val()

                relative_max_x = min(abs(-1 * MAX_ACC - flat_x), MAX_ACC - flat_x)
                relative_max_y = min(abs(-1 * MAX_ACC - flat_y), MAX_ACC - flat_y)

                while not planner.isFinished():
                    start_time = time.clock()
                    retval, self._current_image = camera.read()
                    if not retval:
                        raise IOError("Failed to read image from camera.")

                    ball_x, ball_y = ball_finder.findBall(self._current_image)

                    print "Ball: x: {0}, y: {1}".format(ball_x, ball_y)
                    acc_x, acc_y = planner.getAcceleration(ball_x, ball_y)
                    print "Acc: x: {0}, y: {1}".format(acc_x, acc_y)

                    try:
                        # Check connection
                        if conn.is_connected():
                            new_x_acc = max(-1 * MAX_ACC, min(MAX_ACC, acc_x * ACC_MULTIPLIER + flat_x))
                            new_y_acc = max(-1 * MAX_ACC, min(MAX_ACC, acc_y * ACC_MULTIPLIER + flat_y))
                            conn.set_x_val(new_x_acc)
                            conn.set_y_val(new_y_acc)

                        else:
                            raise SerialException("Lost connection to board.")

                    except SerialException as e:
                        print(e)

                    self.update_callback(self)

                    time.sleep(1.0 / FRAMERATE - (time.clock() - start_time))

                self._finished = planner.isFinished()

            # TODO: Release camera under all circumstances
            camera.release()

    def is_finished(self):
        """
        Returns a boolean value indicating whether the maze has been solved or not. If run() has
        not been called, this method will return False.
        """
        return self._finished

    def get_play_mask(self):
        """
        Returns an opencv mask showing the play space.
        """
        return self._play_mask

    def get_start_mask(self):
        """
        Returns an opencv mask showing the start (ball).
        """
        return self._start_mask

    def get_end_mask(self):
        """
        Returns an opencv mask showing the end of the maze.
        """
        return self._end_mask

    def get_image(self):
        """
        Returns the most recent image.
        """
        return self._current_image

    def get_path(self):
        """
        Returns a list of node objects that represent the ball path.
        """
        return self._path

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
                "start_upper=", "start_lower=", "end_upper=", "end_lower="])
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

    solver.run()
