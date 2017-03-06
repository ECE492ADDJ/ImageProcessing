"""
Filename:       SerialException.py
File type:      server-side python code
Author:         Dominic Trottier
Description:    Custom exceptions for serial communication
"""

class SerialException(Exception):
	pass

class NoResponseException(SerialException):
	pass

class InvalidResponseException(SerialException):
	pass


if __name__ == '__main__':
	pass
