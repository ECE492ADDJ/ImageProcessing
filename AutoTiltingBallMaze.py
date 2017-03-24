"""
Filename:       Gui.py
File type:      server-side python code
Author:         Jake Charlebois
Created on:     2017-03-19
Modified on:    2017-03-19
Description:    Overhead code to call the Gui and other classes used
"""

from Tkinter import *
from StopWatch import StopWatch
from PIL import Image, ImageTk
from StopWatch import StopWatch
import tkMessageBox
import cv2
import sys
import glob
import serial

root = Tk()
root.title("Auto Tilting Ball Maze")
root.configure(bg="#007777")

# Make fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) 


def grabVariables():
	playSpaceUpper = playSpaceEntry1.get()
	playSpaceLower = playSpaceEntry2.get()
	startUpper = startEntry1.get()
	startLower = startEntry2.get()
	endUpper = endEntry1.get()
	endLower = endEntry2.get()
	serialPort = portNum.get()
	camIndex = cameraIndex.get()

	# solver = MazeSolver()


def serial_ports():
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


def detectNumCameras():
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


def checkCamera():	
	#Capture video frames
	cap = cv2.VideoCapture(cameraIndex.get())

# Labels
Label(root, text="Please Enter Variables", font=("Helvetica", 18), bg="#007777").grid(row=0, columnspan=3)
Label(root, text="Upper (as B,G,R)", font=("Helvetica", 18), bg="#007777").grid(row=1, column=1)
Label(root, text="Lower (as B,G,R)", font=("Helvetica", 18), bg="#007777").grid(row=1, column=2)
Label(root, text="PlaySpace Thresholds", font=("Helvetica", 16), bg="#007777").grid(row=2, sticky=E)
Label(root, text="Start Thresholds", font=("Helvetica", 16), bg="#007777").grid(row=3, sticky=E)
Label(root, text="End Thresholds", font=("Helvetica", 16), bg="#007777").grid(row=4, sticky=E)
Label(root, text="Serial Ports",font=("Helvetica", 16), bg="#007777").grid(row=5, sticky=E)
Label(root, text="Camera",font=("Helvetica", 16), bg="#007777").grid(row=6, sticky=E)
Label(root, text="  ", bg="#007777").grid(row=7, sticky=E)

# Text Fields
playSpaceEntry1 = Entry(root)
playSpaceEntry1.grid(row=2,column=1)
playSpaceEntry2 = Entry(root)
playSpaceEntry2.grid(row=2,column=2)
startEntry1 = Entry(root)
startEntry1.grid(row=3,column=1)
startEntry2 = Entry(root)
startEntry2.grid(row=3,column=2)
endEntry1 = Entry(root)
endEntry1.grid(row=4,column=1)
endEntry2 = Entry(root)
endEntry2.grid(row=4,column=2)

# Drop down serial port menu 
portNumbers = serial_ports()
portNumbers.append('1')
portNumbers.append('2')
portNumbers.append('3')

portNum = StringVar(root)
portNum.set("Please select a port")
dropPort = apply(OptionMenu, (root, portNum) + tuple(portNumbers))
dropPort.grid(row=5, column=1, columnspan=2)

# Camera Menu		
indexes = detectNumCameras()
camIndex = []
for n in xrange(indexes):
	camIndex.append(n)

cameraIndex = StringVar(root)
cameraIndex.set(0)
dropCamera = apply(OptionMenu, (root, cameraIndex) + tuple(camIndex))
dropCamera.grid(row=6, column=1)
Button(root, text="Check", font=("Helvetica", 16), command=checkCamera).grid(row=6, column=2)#lambda: checkCamera(master))

# Solve Button
Button(root, text="                    Solve!                    ", command=grabVariables, font=("Helvetica", 16)).grid(row=8, column=0, columnspan=3, rowspan=2)

#Camera Panel
imageFrame = Frame(root, width=600, height=500)
imageFrame.grid(row=0, column=4, rowspan=8)
lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

try:
	show_frame()
except:
	print("Camera not connected")


# Grid Sizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.rowconfigure(9, weight=1)
root.columnconfigure(4, weight=1)

#Stopwatch Timer
sw = StopWatch(root)
sw.configure(bg="#007777")
sw.grid(row=6, column=4)
Button(root, text='Start', command=sw.Start).grid(row=7, column=4, sticky=S)
Button(root, text='Stop', command=sw.Stop).grid(row=8, column=4)
Button(root, text='Reset', command=sw.Reset).grid(row=9, column=4, sticky=N)

# Info box reminder to level the playing surface
tkMessageBox.showinfo("Step 1", "Please manually level the play surface . . .")
root.mainloop()
