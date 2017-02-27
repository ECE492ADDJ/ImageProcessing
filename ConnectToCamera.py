"""
By:     Andrea McIntosh
Date:   2017-02-08
Function: Connect to webcam and take images
"""

# John Montgomery, http://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python, 2017-02-08
import cv2

key = None

def captureVideo():
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(2) # 2 is camera number (0 is computer webcam, 1 is "YouCam")

    # Capture video
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break
    cv2.destroyWindow("preview")

def captureImage():
    # Take a picture
    # Darshan Chaudhary, http://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam, 2017-02-08
    s, im = vc.read() # captures image
    # cv2.imshow("Test Picture", im) # displays captured image
    return im
