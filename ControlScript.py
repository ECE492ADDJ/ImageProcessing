"""
Filename:       ControlScript.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-26
Modified on:    2017-02-26
Description:    Server script running the control loop
"""

from ConnectToCamera import *
from ImageProcessingFunctions import *
from MazeNodes import MazeNodes

def main():
    # image = captureImage()
    image = getImage('maze_square_medium.png')
    mn = MazeNodes(image)
    mn.runProcessing()

if __name__ == '__main__':
    main()
