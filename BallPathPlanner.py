#pylint: disable=C0330,C0103

"""
Filename:       BallPathPlanner.py
File type:      server-side python code
Author:         Dominic Trottier
Description:    This file contains the relevant code for planning and following a path through a
maze.
"""
import time
from math import sqrt
import collections
import Node

class BallPathPlanner(object):
    """
    This class uses an ordered list of nodes to plan a path for the ball to follow as it moves through
    the maze. This class has the following members:

    lookahead: The number of consecutive nodes that are used in calculating the velocity for a
    given node.

    weightingFactor: A number between 0 and 1 that determines the weight placed on nearby nodes
    compared to farther nodes. A higher number leads to more weight being placed on closer nodes.

    speed: The desired speed of the ball, measured in pixels per second.

    proxThreshold: How close (in number of pixels) the ball needs to get to a node before it can
    start moving to the next node.

    latency: The expected latency between a command being sent and the change in acceleration being
    effected measured in seconds.

    pos_queue_size: Determines the size of the queue that stores past positions. This queue is used
    to mitigate the effect of bouncing off of walls on the percieved velocity

    failure_timeout: If the ball does not get to a new node in this amount of time, the target node
    will be set to the previous node
    """
    def __init__(self, nodes):
        self._nodes = nodes
        self.lookahead = 2
        self.weightingFactor = 0.95
        self.speed = 50
        self.proxThreshold = 20
        self.latency = 0.01
        self.pos_queue_size = 10
        self.failure_timeout = 6

        self._finished = False
        self._last_x = None
        self._last_y = None
        self._last_acc_x = 0
        self._last_acc_y = 0
        self._last_time = None
        self._current_node_index = 0
        self._positions = collections.deque(maxlen=self.pos_queue_size)
        self._last_success_time = None

    def getAcceleration(self, ball_x, ball_y):
        """
        Gets the acceleration required for the ball follow the planned path based on the current
        ball position. The acceleration is measured in pixels per second squared. This function
        must be called on a regular and frequent basis to work correctly.

        ball_x: Horizontal position of the ball in pixels.

        ball_y: Vertical position of the ball in pixels.
        """
        if self._last_success_time is None:
            self._last_success_time = time.clock()

        self._positions.append((ball_x, ball_y))
        sums = reduce(lambda pos1, pos2: (pos1[0] + pos2[0], pos1[1] + pos2[1]), self._positions)
        ball_x = sums[0] / len(self._positions)
        ball_y = sums[1] / len(self._positions)

        curr = time.clock()
        if self._last_time is None:
            vel = (0, 0)
        else:
            vel = ((ball_x - self._last_x) / ((curr - self._last_time) * self.pos_queue_size),
                    (ball_y - self._last_y) / ((curr - self._last_time) * self.pos_queue_size))

        expected_ball_x = ball_x + vel[0] * self.latency
        expected_ball_y = ball_y + vel[1] * self.latency

        desired_vel = self._calculateVelocity(expected_ball_x,
                                        expected_ball_y, self._current_node_index)

        if self._last_time is None:
            new_acc = (desired_vel[0], desired_vel[1])
        else:
            dt = curr - self._last_time
            new_acc = ((desired_vel[0] - vel[0]) / dt, (desired_vel[1] - vel[1]) / dt)

        currentnode = self._nodes[self._current_node_index]
        dx = ball_x - currentnode.coordinates[0]
        dy = ball_y - currentnode.coordinates[1]

        if sqrt(dx * dx + dy * dy) <= self.proxThreshold:
            self._last_success_time = curr
            self._current_node_index += 1

        if self._current_node_index == len(self._nodes):
            # Final node, we made it!
            self._finished = True
            return (0, 0)

        if curr - self._last_success_time > self.failure_timeout:
            self._last_success_time = time.clock()
            self._current_node_index -= 1

        self._last_x = ball_x
        self._last_y = ball_y
        self._last_time = time.clock()

        acc = (0.5 * new_acc[0] + 0.5 * desired_vel[0] / self.speed, 0.5 * new_acc[1] + 0.5 * desired_vel[1] / self.speed)
        self._last_acc_x = new_acc[0]
        self._last_acc_y = new_acc[1]


        print "acc: ({0:5.0f}, {1:5.0f}) pos: ({2:3.0f}, {3:3.0f}) target:({4:3.0f}, {5:3.0f})".format(new_acc[0], new_acc[1], ball_x, ball_y, self._nodes[self._current_node_index].coordinates[0], self._nodes[self._current_node_index].coordinates[1])

        return new_acc

    def isFinished(self):
        """
        Returns a boolean value indicating whether the end of the path has been reached.
        """
        return self._finished

    def _calculateVelocity(self, ball_x, ball_y, node_idx):
        """
        Calculates the desired velocity based on the set of nodes and the current ball position.
        """

        # Ineffecient, each calculation is done 5 times.
        ballnode = Node.Node()
        ballnode.coordinates = (ball_x, ball_y)
        curnodes = [ballnode] + self._nodes[node_idx:node_idx + self.lookahead + 1]
        temp_vel = [(curnodes[i + 1].coordinates[0] - curnodes[i].coordinates[0],
                        curnodes[i + 1].coordinates[1] - curnodes[i].coordinates[1])
                        for i in range(len(curnodes) - 1)]

        vel = reduce(lambda v1, v2: \
                        ((1 - self.weightingFactor) * v1[0] + self.weightingFactor * v2[0],
                        (1 - self.weightingFactor) * v1[1] + self.weightingFactor * v2[1]),
                        temp_vel[::-1])

        return (vel[0] / sqrt(vel[0] * vel[0] + vel[1] * vel[1]) * self.speed,
                        vel[1] / sqrt(vel[0] * vel[0] + vel[1] * vel[1]) * self.speed)
