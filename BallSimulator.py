#pylint: disable=C0330,C0103,E1101

"""
Filename:       BallPathPlanner.py
File type:      server-side python code
Author:         Dominic Trottier
Description:    This files contains the revelant code for simulating the ball position in the maze.
"""
import sys
import time
import cv2
import BallPathPlanner as bpp
import Node
from MazeNodes import MazeNodes
from PathFinder import PathFinder
import ImageProcessingFunctions as imgpro

BALL_COLOUR = (66, 134, 244)

class BallSimulator(object):
    """
    Simulates a ball in a maze by allowing the acceleration to be set and tracks the ball position
    according to that acceleration.

    simulate_latency: A boolean value indicating whether latency should be simulated or not.
    Defaults to True.

    latency: The latency in seconds, if sim_latency is True.
    """
    def __init__(self, ball_x, ball_y):
        self._ball_x = ball_x
        self._ball_y = ball_y
        self._vel_x = 0
        self._vel_y = 0
        self._acc_x = 0
        self._acc_y = 0
        self._last_time = time.clock()

        self.simulate_latency = True
        self.latency = 0.005

    def getBallPos(self):
        """
        Gets the simulated position of the ball based on the given acceleration. Returns the
        position as a tuple in the form (x, y).
        """
        self._updateBallPos()

        return (self._ball_x, self._ball_y)

    def setAcceleration(self, acc_x, acc_y):
        """
        Changes the acceleration to a new value. This method will block while simulating latency.

        acc_x: Horizontal acceleration measured in pixels per second squared.

        acc_y: Vertical acceleration measured in pixels per second squared.
        """
        if self.simulate_latency:
            #threading.Timer(self.latency, self._setAccelerationNow, [acc_x, acc_y])
            latency_start = time.clock()
            while time.clock() - latency_start < self.latency:
                pass
            self._setAccelerationNow(acc_x, acc_y)
        else:
            self._setAccelerationNow(acc_x, acc_y)

    def _setAccelerationNow(self, acc_x, acc_y):
        self._updateBallPos()

        self._acc_x = acc_x
        self._acc_y = acc_y

    def _updateBallPos(self):
        curr = time.clock()
        dt = curr - self._last_time
        self._ball_x += self._vel_x * dt + self._acc_x * dt * dt
        self._ball_y += self._vel_y * dt + self._acc_y * dt * dt
        self._vel_x = self._acc_x * dt
        self._vel_y = self._acc_y * dt

        self._last_time = curr


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Invalid arguments. Usage: python BallSimulator.py [image]"
        print "Continuing with hard coded image file..."
        imagepath = "paintmaze_medium.png"
    else:
        imagepath = sys.argv[1]

    image = cv2.imread(imagepath)

    # Run initial image processing
    mn = MazeNodes(image)
    mn.runProcessing()

    nodes = mn.nodes

    startNode = Node.Node()
    endNode = Node.Node()

    for n in nodes:
        if nodes.get(n).start:
            startNode = nodes.get(n)
        if nodes.get(n).end:
            endNode = nodes.get(n)

    imgpro.findRegionCenterNeighbours(startNode, nodes, mn.x_div_len, mn.y_div_len)
    imgpro.findRegionCenterNeighbours(endNode, nodes, mn.x_div_len, mn.y_div_len)

    pf = PathFinder(nodes, startNode, endNode)
    path = pf.findPath()

    planner = bpp.BallPathPlanner(path)
    planner.speed = 400
    ballsim = BallSimulator(startNode.coordinates[0], startNode.coordinates[1])

    while not planner.isFinished():
        start = time.clock()

        x, y = ballsim.getBallPos()
        #print "X: {0:6}, Y: {1:6}".format(x, y)
        cv2.circle(image, (int(x), int(y)), 8, BALL_COLOUR)
        acc = planner.getAcceleration(x, y)
        ballsim.setAcceleration(acc[0], acc[1])

        time.sleep(max(0.03 - (time.clock() - start), 0))

    cv2.imshow("Result", image)
    cv2.waitKey(0)
