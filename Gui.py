"""
Filename:       Gui.py
File type:      server-side python code
Author:         Jake Charlebois
Created on:     2017-03-19
Modified on:    2017-03-19
Description:    Gui for entire project
"""

from Tkinter import *
from MazeSolver import MazeSolver
from PIL import Image, ImageTk
from StopWatch import StopWatch
import cv2
import numpy as np
import sys
import glob
import serial


class Gui:

	def __init__(self, master):

		frame = Frame(master, bg="#006666")
		frame.grid(row=0, column=0, rowspan=1, columnspan=1)

		# Labels
		Label(frame, text="Please Enter Variables", font=("Helvetica", 18), bg="#006666").grid(row=0, columnspan=3)
		Label(frame, text="Upper (as B,G,R)", font=("Helvetica", 18), bg="#006666").grid(row=1, column=1)
		Label(frame, text="Lower (as B,G,R)", font=("Helvetica", 18), bg="#006666").grid(row=1, column=2)
		Label(frame, text="PlaySpace Thresholds", font=("Helvetica", 16), bg="#006666").grid(row=2, sticky=E)
		Label(frame, text="Start Thresholds", font=("Helvetica", 16), bg="#006666").grid(row=3, sticky=E)
		Label(frame, text="End Thresholds", font=("Helvetica", 16), bg="#006666").grid(row=4, sticky=E)
		Label(frame, text="Serial Ports",font=("Helvetica", 16), bg="#006666").grid(row=5, sticky=E)
		Label(frame, text="Camera",font=("Helvetica", 16), bg="#006666").grid(row=6, sticky=E)
		Label(frame, text="  ", bg="#006666").grid(row=7, sticky=E)

		# Text Fields
		self.playSpaceEntry1 = Entry(frame)
		self.playSpaceEntry1.grid(row=2,column=1)
		self.playSpaceEntry2 = Entry(frame)
		self.playSpaceEntry2.grid(row=2,column=2)
		self.startEntry1 = Entry(frame)
		self.startEntry1.grid(row=3,column=1)
		self.startEntry2 = Entry(frame)
		self.startEntry2.grid(row=3,column=2)
		self.endEntry1 = Entry(frame)
		self.endEntry1.grid(row=4,column=1)
		self.endEntry2 = Entry(frame)
		self.endEntry2.grid(row=4,column=2)

		# Drop down menu 
		portNumbers = self.serial_ports()
		portNumbers.append('1')
		portNumbers.append('2')
		portNumbers.append('3')

		print(portNumbers)
		self.portNum = StringVar(frame)
		self.portNum.set("Please select a port")
		dropPort = apply(OptionMenu, (frame, self.portNum) + tuple(portNumbers))
		dropPort.grid(row=5, column=1, columnspan=2)

		# Camera Menu		
		indexes = self.detectNumCameras()
		print(indexes)
		camIndex = []
		for n in xrange(indexes):
			camIndex.append(n)

		self.cameraIndex = StringVar(frame)
		self.cameraIndex.set("Please select a port")
		dropCamera = apply(OptionMenu, (frame, self.cameraIndex) + tuple(camIndex))
		dropCamera.grid(row=6, column=1)
		Button(frame, text="Check", font=("Helvetica", 16)).grid(row=6, column=2)#lambda: self.checkCamera(master))  , command=self.videoLoop

		# Solve Button
		Button(frame, text="                    Solve!                    ", command=self.grabVariables, font=("Helvetica", 16)).grid(row=8, column=0, columnspan=5)

		# Grid Sizing
		frame.columnconfigure(0, weight=1)
		frame.rowconfigure(0, weight=1)
		frame.columnconfigure(1, weight=1)
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(2, weight=1)
		frame.rowconfigure(2, weight=1)
		frame.columnconfigure(3, weight=1)
		frame.rowconfigure(3, weight=1)
		frame.rowconfigure(4, weight=1)
		frame.rowconfigure(5, weight=1)
		frame.rowconfigure(6, weight=1)
		frame.rowconfigure(7, weight=10)
		frame.rowconfigure(8, weight=1)


	def grabVariables(self):
		playSpaceUpper = self.playSpaceEntry1.get()
		playSpaceLower = self.playSpaceEntry2.get()
		startUpper = self.startEntry1.get()
		startLower = self.startEntry2.get()
		endUpper = self.endEntry1.get()
		endLower = self.endEntry2.get()
		serialPort = self.portNum.get()
		camIndex = self.cameraIndex.get()

		# solver = MazeSolver()

	def serial_ports(self):
	    if sys.platform.startswith('win'):
	        ports = ['COM%s' % (i + 1) for i in range(256)]
	    elif sys.platform.startswith ('linux'):
        	temp_list = glob.glob ('/dev/tty[A-Za-z]*')
	    result = []
	    for a_port in temp_list:
	        try:
	            s = serial.Serial(a_port)
	            s.close()
	            result.append(a_port)
	        except serial.SerialException:
	            pass
	    return result  


	def detectNumCameras(self):
		
		ind = 0
		# Iterates through indexes until we cant find a camera
		while True:
		    vc = cv2.VideoCapture(ind)
		    if (vc.isOpened()):
		    	ind += 1
		        vc.release()
		    else:
		    	break

		return ind