# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

# load the image
image = cv2.imread("./paintmaze_small.jpg")

# define the list of colour ranges
boundaries =  [([240, 240, 240], [255, 255, 255])] # white

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # # http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html, 2017-02-02
    # im2, contours, heiarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image, contours, -1, (255, 0, 0), 3)

    # http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/, 2017-02-02
    edges = cv2.Canny(image, 225, 250) # element of edges represents pixels in a row (width)

    starts = {}
    ends = {}
    for row_i in range(0, len(edges)):
        if 255 in edges[row_i]:
            pix_i = 0
            while pix_i < len(edges[row_i]):
                start = pix_i
                while (edges[row_i][pix_i] == 255):
                    pix_i += 1
                if pix_i > (start + 10):
                    if row_i not in starts:
                        starts[row_i] = []
                        ends[row_i] = []
                    starts[row_i].append(start)
                    ends[row_i].append(pix_i)
                pix_i += 1
            # break

    print starts, ends

    # # # show the images
    cv2.imshow("images", np.hstack([image[:,:,1], edges]))
    cv2.waitKey(0)
