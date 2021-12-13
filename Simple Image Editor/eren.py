# Eren's initial work file
# can create new files when necessary

from matplotlib import pyplot as plot, image as img
from PIL import Image
import numpy as np
import cv2


def IsGrayScale():
    if(len(image.shape) < 3): return True
    if(image.shape[2] == 1): return True

    sourceImage = Image.fromarray(image, "RGB")
    width, height = sourceImage.size
    for i in range(width):
        for j in range(height):
            r, g, b = sourceImage.getpixel((i, j))
            if r != g != b:
                return False
    return True


def ConvertToGrayScale():
    if (IsGrayScale()):
        print("ConvertToGrayScale: The source image is already grayscale! Please be sure to give a proper colorful image.")
        return image
    else:
        print("ConvertToGrayScale: The source image is converted to grayscale successfully.")
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def ShowImage(sourceImage):
    if(IsGrayScale()):
        print("ShowImage: (1 channel) Grayscale image received. Showing image.")
        plot.imshow(cv2.cvtColor(sourceImage, cv2.COLOR_GRAY2RGB))
        plot.show()
    else:
        print("ShowImage: (3 channel) RGB image received. Showing image.")
        plot.imshow(sourceImage)
        plot.show()


image = img.imread("Sharbat Gula, the Afghan Girl.jpg")
ShowImage(image)

image = ConvertToGrayScale()
ShowImage(image)
