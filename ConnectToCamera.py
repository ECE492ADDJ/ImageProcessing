"""
Filename:       ConnectToCamera.py
File type:      server-side python code
Author:         Andrea McIntosh
Created on:     2017-02-08
Modified on:    2017-02-26
Description:    Functions for connecting to the usb webcam and capturing images
"""
import cv2

def connectCamera():
    cameraIndex = findCameraIndex()
    # John Montgomery, http://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python, 2017-02-08
    vc = cv2.VideoCapture(cameraIndex)
    return vc

def releaseCamera(vc):
    vc.release()

def captureVideo(vc):
    """
    Connect to camera, capture and display a video frame-by-frame
    """
    cv2.namedWindow("preview")
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
    cv2.destroyWindow("preview")

def captureImage(vc):
    """
    Connect to camera, take and display a single image

    Output: image captured by camera
    """
    if vc.isOpened():
        s, im = vc.read() # captures image
    else:
        im = None
    # Test: Display captured image
    # cv2.imshow("preview", im)
    # cv2.imwrite('maze_photo.png', im)
    return im

def findCameraIndex():
    """
    Find the index of the usb camera.  This function assumes that the usb camera is indexed last out
    of all connectable cameras.

    Output: camera index for OpenCV to connect to
    """
    ind = 0
    # Iterate through indexes until one does not open a valid camera object
    while True:
        vc = cv2.VideoCapture(ind)
        if vc.isOpened():
            vc.release()
            ind += 1
        else:
            # Once an invalid index is reached, return previous valid index
            return ind - 1
            # return 0
