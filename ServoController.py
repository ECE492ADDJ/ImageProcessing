"""
Filename:       ServoController.py
File type:      server-side python code
Author:         Dominic Trottier
Description:    Allows you to control servos over serial port
"""

import serial
import sys
import re
from SerialException import SerialException, NoResponseException, InvalidResponseException

class ServoConnection:
    # A better solution could be implemented by creating a class for commands,
    # but this should be good for the current purposes.
    __MSG_OPEN_CHAR = '<'
    __MSG_CLOSE_CHAR = '>'

    __ACK_STR    = "ACK"
    __NACK_STR = "NACK"

    __CMD_PING = "PG"
    __CMD_SETX = "SX"
    __CMD_SETY = "SY"
    __CMD_GETX = "GX"
    __CMD_GETY = "GY"

    def __init__(self, port='/dev/ttyUSB0', timeout=0.05):
        self.serconn = serial.Serial(port, 57600, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.serconn.is_open:
            self.serconn.close()

    def is_connected(self):
        if not self.serconn.is_open:
            self.serconn.open()

        self.serconn.write(self.__MSG_OPEN_CHAR + self.__CMD_PING + self.__MSG_CLOSE_CHAR)

        resp = self.serconn.read_until(self.__MSG_CLOSE_CHAR)

        return resp == self.__MSG_OPEN_CHAR + self.__ACK_STR + self.__MSG_CLOSE_CHAR

    def get_x_val(self):
        """ Get the current position of the 'x' servo """
        if not self.serconn.is_open:
            self.serconn.open()

        self.serconn.write(self.__MSG_OPEN_CHAR + self.__CMD_GETX + self.__MSG_CLOSE_CHAR)

        resp = self.serconn.read_until(self.__MSG_CLOSE_CHAR)
        match = re.search(self.__CMD_GETX + "([0-9a-f]{4})", resp)

        if resp == "":
            raise NoResponseException("No response received for GETX.")

        if match is None:
            raise InvalidResponseException("Argument not found in GETX response.")

		# Compensation for servo orientation
        return -1 * twos_comp(int(match.group(1), 16), 16)

    def get_y_val(self):
        """ Get the current position of the 'y' servo """
        if not self.serconn.is_open:
            self.serconn.open()

        self.serconn.write(self.__MSG_OPEN_CHAR + self.__CMD_GETY + self.__MSG_CLOSE_CHAR)

        resp = self.serconn.read_until(self.__MSG_CLOSE_CHAR)
        match = re.search(self.__CMD_GETY + "([0-9a-f]{4})", resp)

        if resp == "":
            raise NoResponseException("No response received for GETY.")

        if match is None:
            raise InvalidResponseException("Argument not found in GETY response.")

        return twos_comp(int(match.group(1), 16), 16)

    def set_x_val(self, val):
        """ Set the new position of the 'x' servo """
        if not self.serconn.is_open:
            self.serconn.open()

        # Compensation for servo orientation
        val = -1 * val

        if val < 0:
            val = val + 2 ** 16

        self.serconn.write(self.__MSG_OPEN_CHAR + self.__CMD_SETX + '%04x' % val + self.__MSG_CLOSE_CHAR)

        resp = self.serconn.read_until(self.__MSG_CLOSE_CHAR)

        if resp == "":
            raise NoResponseException("No response received for SETX.")
        elif resp != self.__MSG_OPEN_CHAR + self.__ACK_STR + self.__MSG_CLOSE_CHAR:
            raise InvalidResponseException("SETX not acknowledged.")

    def set_y_val(self, val):
        """ Set the new position of the 'y' servo """
        if not self.serconn.is_open:
            self.serconn.open()

        if val < 0:
            val += 2 ** 16

        self.serconn.write(self.__MSG_OPEN_CHAR + self.__CMD_SETY + '%04x' % val + self.__MSG_CLOSE_CHAR)

        resp = self.serconn.read_until(self.__MSG_CLOSE_CHAR)

        if resp == "":
            raise NoResponseException("No response received for SETY.")
        elif resp != self.__MSG_OPEN_CHAR + self.__ACK_STR + self.__MSG_CLOSE_CHAR:
            raise InvalidResponseException("SETY not acknowledged.")


# Source: http://stackoverflow.com/a/9147327
def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


if __name__ == '__main__':
    with ServoConnection() as conn:
        while(True):
            text = raw_input("Enter command: ")

            cmd, sep, arg = text.partition(" ")

            arg = int(arg) if arg != "" else -1

            if cmd == "exit":
                break

            elif cmd == "testconn":
                print "Connected: {0}".format(conn.is_connected())

            elif cmd == "setx":
                if arg == -1:
                    print "No argument supplied."
                    continue

                try:
                    conn.set_x_val(arg)
                except NoResponseException:
                    print "No response received."
                    continue
                except InvalidResponseException:
                    print "Response was not ACK."
                    continue

            elif cmd == "sety":
                if arg == -1:
                    print "No argument supplied."
                    continue

                try:
                    conn.set_y_val(arg)
                except NoResponseException:
                    print "No response received."
                    continue
                except InvalidResponseException:
                    print "Response was not ACK."
                    continue

            elif cmd == "getx":
                try:
                    val = conn.get_x_val()
                    print "X: {0}".format(val)
                except NoResponseException:
                    print "No response received."
                    continue
                except InvalidResponseException:
                    print "Response did not contain value."
                    continue
            elif cmd == "gety":
                try:
                    val = conn.get_y_val()
                    print "Y: {0}".format(val)
                except NoResponseException:
                    print "No response received."
                    continue
                except InvalidResponseException:
                    print "Response did not contain value."
                    continue
            else:
                print "Invalid command; try testconn, setx, sety, getx, or gety."
