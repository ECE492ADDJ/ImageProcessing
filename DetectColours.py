# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

SIG_LENGTH = 10

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

    # http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/, 2017-02-02
    edges = cv2.Canny(image, 225, 250) # element of edges represents pixels in a row (width)

    # Dicts to hold starting pixels and end pixels of corners in rows
    starts = {}
    ends = {}
    for row_i in range(0, len(edges)):
        if 255 in edges[row_i]: # If there are any detected edge pixels
            pix_i = 0
            # iterate through all pixels in the row
            while pix_i < len(edges[row_i]):
                start = pix_i
                # Move along an edge in the row, saving the start of the edge
                while (edges[row_i][pix_i] == 255):
                    pix_i += 1
                # If the edge is of significant size (not noise)
                if pix_i > (start + SIG_LENGTH):
                    # Make a list of starts and ends of significant edges in row
                    if row_i not in starts:
                        starts[row_i] = []
                        ends[row_i] = []
                    starts[row_i].append(start)
                    ends[row_i].append(pix_i)
                pix_i += 1

    # for k in starts.keys():
    #     print str(k) + ": "
    #     print starts[k]
    #     print ends[k]

    midlines = []
    # Compute midpoints of each edge, and save pixel indices as tuples
    for k in starts.keys():
        for ind in range(0, len(starts[k])):
            midpoint = int((ends[k][ind] + starts[k][ind]) / 2)
            midlines.append((midpoint, k))

    print midlines

    for ind in range(0, len(midlines) - 1):
        cv2.line(image, midlines[ind], midlines[ind+1], (255, 0, 0))

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)
