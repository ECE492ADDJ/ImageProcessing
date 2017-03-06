"""
Filename:       ConnectToCamera.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-08
Modified on:    2017-02-26
Description:    Functions for connecting to the usb webcam and capturing images
"""
import cv2

def captureVideo():
    """
    Connect to camera, capture and display a video frame-by-frame
    """
    cv2.namedWindow("preview")
    # John Montgomery, http://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python, 2017-02-08
    vc = cv2.VideoCapture(1) # 1 is camera number (0 is computer webcam)

    # Capture video
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    # Continually take and display images to create video feed
    while rval:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            rval = False
            break
    vc.release()
    cv2.destroyWindow("preview")

def captureImage():
    """
    Connect to camera, take and display a single image

    Output: image captured by camera
    """
    # Darshan Chaudhary, http://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam, 2017-02-08
    vc = cv2.VideoCapture(0) # 1 is camera number (0 is computer webcam)
    if vc.isOpened():
        s, im = vc.read() # captures image
    else:
        im = None
    # Test: Display captured image
    cv2.imshow("preview", im)
    vc.release() # release camera capture
    return im
