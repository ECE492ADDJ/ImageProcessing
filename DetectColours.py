# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/, 2017-01-31
# import the necessary packages
import numpy as np
import cv2

# load the image
image = cv2.imread("./paintmaze_small.jpg")

# define the list of colour ranges
boundaries = [
    ([0, 0, 0], [5, 5, 5]),            # black
    ([0, 150, 0], [90, 255, 50]),  # green?
    ([0, 0, 150], [50, 50, 255]),  # red
    ([250, 250, 250], [255, 255, 255]) # white
]

# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)

############### Old just python code
# http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/

# from PIL import Image
# import sys, os, re
#
# def main(argv):
#     fpath, ext = os.path.splitext(argv[0])
#     fname = re.search('([\\/]\w+$)', fpath).group(0)
#     img = Image.open(argv[0])
#     currdir = os.path.dirname(os.path.realpath(__file__))
#
#     # # http://stackoverflow.com/questions/1065945/how-to-reduce-color-palette-with-pil, 2017-01-26
#     # result = img.convert('P', palette=Image.ADAPTIVE, colors=4)
#
#     # tzot, http://stackoverflow.com/questions/236692/how-do-i-convert-any-image-to-a-4-color-paletted-image-using-the-python-imaging-l, 2017-01-26
#     pal_image= Image.new("P", (1,1))
#     pal_image.putpalette( (0,0,0, 0,255,0, 255,0,0, 255,255,0) + (0,0,0)*252)
#     result =  img.convert("RGB").quantize(palette=pal_image)
#
#     result.save(currdir + fname + '_flat' + '.png')
#
# if __name__ == "__main__":
#     # http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html, 2016-05-26
#     main(sys.argv[1:])
