# Eren's initial work file
# can create new files when necessary

from matplotlib import pyplot as plot
from PIL import Image, ImageOps
import numpy as np
import cv2


def IsTransparent(sourceImage):
    if(sourceImage.mode == "RGBA" or "transparency" in sourceImage.info): return True
    else: return False


def IsGrayScale(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3): return True
    if(np.asarray(sourceImage).shape[2] == 1): return True

    width, height = sourceImage.size
    for i in range(width):
        for j in range(height):
            if(IsTransparent(sourceImage)):
                r, g, b, a = sourceImage.getpixel((i, j))
            else:
                r, g, b = sourceImage.getpixel((i, j))
            if r != g != b:
                return False
    return True


def ConvertToGrayScale():
    if(IsGrayScale(image)):
        print("ConvertToGrayScale: The source image is already grayscale! Please be sure to give a proper colorful image.")
        return image
    else:
        print("ConvertToGrayScale: The source image is converted to grayscale successfully.")
        if (IsTransparent(image)):
            return Image.fromarray(cv2.cvtColor(np.asarray(image), cv2.COLOR_RGBA2GRAY))
        return Image.fromarray(cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY))


def InvertImage():
    if(IsTransparent(image)):
        sourceImage = image.convert("RGB")
        print("InvertImage: The transparent source image is inverted successfully.")
        return ImageOps.invert(sourceImage).convert("RGBA")
    else:
        print("InvertImage: The source image is inverted successfully.")
        return ImageOps.invert(image)


def MirrorImage():
    print("MirrorImage: The source image is mirrored successfully.")
    return ImageOps.mirror(image)


def ShowImage(sourceImage):
    if(IsGrayScale(sourceImage)):
        print("ShowImage: Grayscale image received. Showing image.")
        plot.imshow(sourceImage, cmap='gray', vmin=0, vmax=255)
        plot.show()
    elif(IsTransparent(sourceImage)):
        print("ShowImage: (RGBA) Transparent image received. Showing image.")
        plot.imshow(sourceImage)
        plot.show()
    else:
        print("ShowImage: (RGB) Colorful image received. Showing image.")
        plot.imshow(sourceImage)
        plot.show()


image = Image.open("Sharbat Gula, the Afghan Girl.jpg")
ShowImage(image)


image = ConvertToGrayScale()
ShowImage(image)
image = InvertImage()
ShowImage(image)
image = MirrorImage()
ShowImage(image)
