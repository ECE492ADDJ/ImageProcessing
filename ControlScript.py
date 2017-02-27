from ConnectToCamera import *
from ImageProcessingFunctions import *
from MazeNodes import MazeNodes

def main():
    # image = captureImage()
    image = getImage('paintmaze_small.jpg')
    mn = MazeNodes(image)
    mn.runProcessing()

if __name__ == '__main__':
    main()
