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
import cv2
import tkMessageBox


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

		self.frame = Frame(master, bg="green")
		self.frame.pack(fill=BOTH, expand=1)

		# Labels
		Label(self.frame, text="Please Enter Variables", font=("Helvetica", 18), bg="green").grid(row=0, columnspan=3)
		Label(self.frame, text="Upper (as B,G,R)", font=("Helvetica", 18), bg="green").grid(row=1, column=1)
		Label(self.frame, text="Lower (as B,G,R)", font=("Helvetica", 18), bg="green").grid(row=1, column=2)
		Label(self.frame, text="PlaySpace Thresholds", font=("Helvetica", 16), bg="green").grid(row=2, sticky=E)
		Label(self.frame, text="Start Thresholds", font=("Helvetica", 16), bg="green").grid(row=3, sticky=E)
		Label(self.frame, text="End Thresholds", font=("Helvetica", 16), bg="green").grid(row=4, sticky=E)
		Label(self.frame, text="Serial Ports",font=("Helvetica", 16), bg="green").grid(row=5, sticky=E)
		Label(self.frame, text="Camera",font=("Helvetica", 16), bg="green").grid(row=6, sticky=E)
		Label(self.frame, text="  ", bg="green").grid(row=7, sticky=E)

		# Text Fields
		self.playSpaceEntry1 = Entry(self.frame)
		self.playSpaceEntry1.grid(row=2,column=1)
		self.playSpaceEntry2 = Entry(self.frame)
		self.playSpaceEntry2.grid(row=2,column=2)
		self.startEntry1 = Entry(self.frame)
		self.startEntry1.grid(row=3,column=1)
		self.startEntry2 = Entry(self.frame)
		self.startEntry2.grid(row=3,column=2)
		self.endEntry1 = Entry(self.frame)
		self.endEntry1.grid(row=4,column=1)
		self.endEntry2 = Entry(self.frame)
		self.endEntry2.grid(row=4,column=2)

		# Drop down menu 
		self.portNum = StringVar(self.frame)
		self.portNum.set("Please select a port")
		self.dropPort = OptionMenu(self.frame, self.portNum, "one", "two", "three")
		self.dropPort.grid(row=5, column=1, columnspan=2)

		# Camera Menu
		self.cameraIndex = StringVar(self.frame)
		self.cameraIndex.set("Please select a port")
		self.dropCamera = OptionMenu(self.frame, self.cameraIndex, "one", "two", "three")
		self.dropCamera.grid(row=6, column=1)
		self.camButton = Button(self.frame, text="Check", command=self.checkCamera, font=("Helvetica", 16))
		self.camButton.grid(row=6, column=2)

		# Solve Button
		self.btnSolve = Button(self.frame, text="                    Solve!                    ", command=self.grabVariables, font=("Helvetica", 16))
		self.btnSolve.grid(row=8, column=0, columnspan=5)

		# Grid Sizing
		self.frame.columnconfigure(0, weight=1)
		self.frame.rowconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)
		self.frame.rowconfigure(1, weight=1)
		self.frame.columnconfigure(2, weight=1)
		self.frame.rowconfigure(2, weight=1)
		self.frame.columnconfigure(3, weight=10)
		self.frame.rowconfigure(3, weight=1)
		self.frame.rowconfigure(4, weight=1)
		self.frame.rowconfigure(5, weight=1)
		self.frame.rowconfigure(6, weight=1)
		self.frame.rowconfigure(7, weight=10)
		self.frame.rowconfigure(8, weight=1)


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


	def checkCamera(self):
		print("Is this the camera you want to use?")

		# Photo (will be video feed) Still not working...
		photo = PhotoImage(file="paintmaze_small.png")
		label = Label(self.frame, image=photo).grid(row=0, column=3, rowspan=8)

root = Tk()
root.title("Auto Tilting Ball Maze")

# Make fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

app = Gui(root)
tkMessageBox.showinfo("Step 1", "Please manually level the play surface . . .")
root.mainloop()
