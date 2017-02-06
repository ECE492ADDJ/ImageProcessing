# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

SIG_LENGTH = 10

NUM_DIVS = 32

# load the image
image = cv2.imread("./paintmaze_small.jpg")

# define the list of colour ranges
boundaries =  [([240, 240, 240], [255, 255, 255])] # white

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # Convert mask output to greyscale
    # http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html, 2017-02-05
    gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    nodes = []
    x_div = int(len(gray_image[0]) / NUM_DIVS) # floors number of divisions in width
    y_div = int(len(gray_image) / NUM_DIVS) # floors number of divisions in height
    for div_x in range(0, NUM_DIVS):
        for div_y in range(0, NUM_DIVS):
            wall = False
            for y_i in range(div_y*y_div, (div_y+1)*y_div):
                if 0 in gray_image[y_i][div_x*x_div:(div_x+1)*x_div]:
                    wall = True
            if not wall:
                nodes.append((x_div*div_x+(div_x/2), y_div*div_y+(div_y/2)))

    for n in nodes:
        cv2.circle(image, n, 5, (255, 255, 0), -1)

    # # http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/, 2017-02-02
    # edges = cv2.Canny(gray_image, 225, 250) # element of edges represents pixels in a row (width)

    # show the images
    cv2.imshow("images", np.hstack([image]))
    cv2.waitKey(0)

    # cv2.imwrite("maze_points.png", image)


    # # Dicts to hold starting pixels and end pixels of corners in rows
    # row_starts = {}
    # row_ends = {}
    # for row_i in range(0, len(edges)):
    #     if 255 in edges[row_i]: # If there are any detected edge pixels
    #         pix_i = 0
    #         # iterate through all pixels in the row
    #         while pix_i < len(edges[row_i]):
    #             start = pix_i
    #             # Move along an edge in the row, saving the start of the edge
    #             while (edges[row_i][pix_i] == 255):
    #                 pix_i += 1
    #             # If the edge is of significant size (not noise)
    #             if pix_i > (start + SIG_LENGTH):
    #                 # Make a list of row_starts and row_ends of significant edges in row
    #                 if row_i not in row_starts:
    #                     row_starts[row_i] = []
    #                     row_ends[row_i] = []
    #                 row_starts[row_i].append(start)
    #                 row_ends[row_i].append(pix_i)
    #             pix_i += 1
    #
    # # Dicts to hold starting pixels and end pixels of corners in rows
    # col_starts = {}
    # col_ends = {}
    # for col_i in range(0, len(edges[0])): # over number of columns in one row
    #     pix_i = 0
    #     # iterate through all pixels in the col
    #     while pix_i < len(edges):
    #         start = pix_i
    #         # Move down an edge in the col, saving the start of the edge
    #         while (edges[pix_i][col_i] == 255):
    #             pix_i += 1
    #         # If the edge is of significant size (not noise)
    #         if pix_i > (start + SIG_LENGTH):
    #             # Make a list of col_starts and col_ends of significant edges in col
    #             if col_i not in col_starts:
    #                 col_starts[col_i] = []
    #                 col_ends[col_i] = []
    #             col_starts[col_i].append(start)
    #             col_ends[col_i].append(pix_i)
    #         pix_i += 1
    #
    # intersects = []
    # for ci in col_starts.keys():
    #     for ri in row_starts.keys():
    #         intersects.append((ci, ri))
    #
    # # http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
    # for ind in range(0, len(intersects)):
    #     cv2.circle(image, intersects[ind], 5, (255, 0, 0), -1)

    # row_indices = []
    # for y in row_starts.keys():
    #     for x in row_starts[y]:
    #         row_indices.append((x, y))
    # for y in row_ends.keys():
    #     for x in row_ends[y]:
    #         row_indices.append((x, y))
    #
    # col_indices = []
    # for x in col_starts.keys():
    #     for y in col_starts[x]:
    #         col_indices.append((x, y))
    # for x in col_ends.keys():
    #     for y in col_ends[x]:
    #         col_indices.append((x, y))

    # # http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
    # for ind in range(0, len(row_indices)):
    #     cv2.circle(image, row_indices[ind], 10, (255, 0, 0), -1)
    #
    # for ind in range(0, len(col_indices)):
    #     cv2.circle(image, col_indices[ind], 5, (255, 255, 0), -1)

    # midrows = []
    # # Compute midpoints of each edge, and save pixel indices as tuples
    # for k in row_starts.keys():
    #     for ind in range(0, len(row_starts[k])):
    #         midpoint = int((row_ends[k][ind] + row_starts[k][ind]) / 2)
    #         midrows.append((midpoint, k))
    #
    # midcols = []
    # # Compute midpoints of each edge, and save pixel indices as tuples
    # for k in col_starts.keys():
    #     for ind in range(0, len(col_starts[k])):
    #         midpoint = int((col_ends[k][ind] + col_starts[k][ind]) / 2)
    #         midcols.append((k, midpoint))
    #
    # # http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html
    # for ind in range(0, len(midrows)):
    #     cv2.circle(image, midrows[ind], 5, (255, 0, 0), -1)
    #
    # for ind in range(0, len(midcols)):
    #     cv2.circle(image, midcols[ind], 5, (255, 255, 0), -1)



"""

1. Flatten image - make every e.g. 16x16 block the floor/ceiling

2. Find intermediate nodes, too

3. Look at pixel groups that include walls - detect what wall
    shape is around (corner, etc.)

"""
