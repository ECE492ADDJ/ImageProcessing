"""
Filename:       Gui.py
File type:      server-side python code
Author:         Jake Charlebois
Created on:     2017-03-19
Modified on:    2017-03-19
Description:    Gui for entire project
"""

from Tkinter import *
# from MazeSolver import MazeSolver
import cv2
import numpy as np
import tkMessageBox
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import sys
import glob
import serial
import time


class Gui:
	def __init__(self, master):
				
		# # Toolbar
			# toolbar = Frame(master, bg="blue")
			# startMaskbtn = Button(toolbar, text="Start Mask", command=self.grabVariables)
			# startMaskbtn.pack(side=LEFT, padx=2,pady=2)
			# endMaskbtn = Button(toolbar, text="End Mask", command=self.grabVariables)
			# endMaskbtn.pack(side=LEFT, padx=2,pady=2)
			# pathMaskbtn = Button(toolbar, text="Path", command=self.grabVariables)
			# pathMaskbtn.pack(side=LEFT, padx=2,pady=2)
			# toolbar.pack(side=TOP, fill=X)

		frame = Frame(master)
		frame.grid(row=0, column=0, rowspan=9, columnspan=4)
		#frame.pack(fill=BOTH)

		# Labels
		Label(frame, text="Please Enter Variables", font=("Helvetica", 18)).grid(row=0, columnspan=3)
		Label(frame, text="Upper (as B,G,R)", font=("Helvetica", 18)).grid(row=1, column=1)
		Label(frame, text="Lower (as B,G,R)", font=("Helvetica", 18)).grid(row=1, column=2)
		Label(frame, text="PlaySpace Thresholds", font=("Helvetica", 16)).grid(row=2, sticky=E)
		Label(frame, text="Start Thresholds", font=("Helvetica", 16)).grid(row=3, sticky=E)
		Label(frame, text="End Thresholds", font=("Helvetica", 16)).grid(row=4, sticky=E)
		Label(frame, text="Serial Ports",font=("Helvetica", 16)).grid(row=5, sticky=E)
		Label(frame, text="Camera",font=("Helvetica", 16)).grid(row=6, sticky=E)
		Label(frame, text="  ").grid(row=7, sticky=E)

		# Text Fields
		playSpaceEntry1 = Entry(frame)
		playSpaceEntry1.grid(row=2,column=1)
		playSpaceEntry2 = Entry(frame)
		playSpaceEntry2.grid(row=2,column=2)
		startEntry1 = Entry(frame)
		startEntry1.grid(row=3,column=1)
		startEntry2 = Entry(frame)
		startEntry2.grid(row=3,column=2)
		endEntry1 = Entry(frame)
		endEntry1.grid(row=4,column=1)
		endEntry2 = Entry(frame)
		endEntry2.grid(row=4,column=2)

		# Drop down menu 
		portNumbers = self.serial_ports()
		print(portNumbers)
		portNum = StringVar(frame)
		portNum.set("Please select a port")
		dropPort = OptionMenu(frame, portNum, "one", "two", "three")
		dropPort.grid(row=5, column=1, columnspan=2)

		# Camera Menu
		cameraIndex = StringVar(frame)
		cameraIndex.set("Please select a port")
		dropCamera = OptionMenu(frame, cameraIndex, "one", "two", "three")
		dropCamera.grid(row=6, column=1)
		camButton = Button(frame, text="Check", command=lambda: self.checkCamera(master), font=("Helvetica", 16))
		camButton.grid(row=6, column=2)

		# Video Capture
		# img = ImageTk.PhotoImage(Image.open("paintmaze_medium.jpg"))
		# panel = Label(frame, image = img).grid(row=0, column=3, sticky=N+E+S+W, rowspan=8)

		# Solve Button
		btnSolve = Button(frame, text="                    Solve!                    ", command=self.grabVariables, font=("Helvetica", 16))
		btnSolve.grid(row=8, column=0, columnspan=5)

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

	#	solver = MazeSolver(--image, camIndex, serialPort, playSpaceUpper, playSpaceLower, startUpper, startLower, endUpper, endLower)


	def checkCamera(self, frame):
		print("Is this the camera you want to use?")
		img = ImageTk.PhotoImage(Image.open("paintmaze_medium.jpg"))
		panel = Label(frame, image = img).grid(row=0, column=4, sticky=N+E+S+W, rowspan=9)

# The following was found at http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
	def serial_ports(self):
	    """ Lists serial port names

	        :raises EnvironmentError:
	            On unsupported or unknown platforms
	        :returns:
	            A list of the serial ports available on the system
	    """
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


# This StopWatch Class copied from http://code.activestate.com/recipes/124894-stopwatch-in-tkinter/
class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()      

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)                      
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)
        

root = Tk()
root.title("Auto Tilting Ball Maze")

# Make fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

app = Gui(root)
sw = StopWatch(root)
sw.grid(row=1, column=4)

Button(root, text='Start', command=sw.Start).grid(row=2, column=4)
Button(root, text='Stop', command=sw.Stop).grid(row=3, column=4)
Button(root, text='Reset', command=sw.Reset).grid(row=4, column=4)

img = ImageTk.PhotoImage(Image.open("paintmaze_medium.jpg"))
Label(root, image = img).grid(row=0, column=4, sticky=N+E+S+W)

tkMessageBox.showinfo("Step 1", "Please manually level the play surface . . .")
root.mainloop()
