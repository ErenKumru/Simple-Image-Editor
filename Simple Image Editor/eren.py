# Eren's initial work file
# can create new files when necessary

from matplotlib import pyplot as plot
from PIL import Image, ImageOps
from skimage.util import random_noise
import numpy as np
import cv2


def IsTransparent(sourceImage):
    if(sourceImage.mode == "RGBA" or "transparency" in sourceImage.info): return True
    else: return False


def NumberOfChannels(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3):
        return 1
    return np.asarray(sourceImage).shape[2]


def IsGrayScale(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3): return True
    if(NumberOfChannels(sourceImage) == 1): return True

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
        return image.convert("L")#.convert(image.mode) can be used to preserve number of channels


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


def AddNoise(mode="gaussian", var=0.01, amount=0.05):
    """
    https://scikit-image.org/docs/stable/api/skimage.util.html#random-noise
    One of the following strings, selecting the type of noise to add:
        "gaussian" Gaussian-distributed additive noise.
        "poisson" Poisson-distributed noise generated from the data.
        "salt" Replaces random pixels with 1.
        "pepper" Replaces random pixels with 0 (for unsigned images) or -1 (for signed images).
        "s&p" Replaces random pixels with either 1 or low_val, where low_val is 0 for unsigned images or -1 for signed images.
        "speckle" Multiplicative noise using out = image + n*image, where n is Gaussian noise with specified mean & variance.
    """

    sourceImage = image

    if(IsGrayScale(sourceImage) and NumberOfChannels(sourceImage) > 1):
        sourceImage = sourceImage.convert("L")

    # random_noise() method will convert image in [0, 255] to [0, 1.0]
    # inherently it uses np.random.normal() to create normal distribution and adds the generated noised back to image
    if(mode == "gaussian"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, var=var)
    elif(mode == "poisson"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode)
    elif(mode == "salt"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "pepper"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "s&p"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, amount=amount)
    elif(mode == "speckle"):
        noiseImage = random_noise(np.asarray(sourceImage), mode=mode, var=var)
    else:
        print("AddNoise: Noise mode does not exist! No noise added.")
        return sourceImage

    print("AddNoise: The", mode, "noise is added to the source image successfully.")
    noiseImage = (255 * noiseImage).astype(np.uint8)
    return Image.fromarray(noiseImage)#.convert(image.mode) can be used to preserve number of channels


def ShowImage(sourceImage):
    if(IsGrayScale(sourceImage)):
        print("ShowImage: ({} channel) Grayscale image received. Showing image.".format(NumberOfChannels(sourceImage)))
        plot.imshow(sourceImage, cmap='gray', vmin=0, vmax=255)
        plot.show()
    elif(IsTransparent(sourceImage)):
        print("ShowImage: ({} channel) Transparent image received. Showing image.".format(NumberOfChannels(sourceImage)))
        plot.imshow(sourceImage)
        plot.show()
    else:
        print("ShowImage: ({} channel) Colorful image received. Showing image.".format(NumberOfChannels(sourceImage)))
        plot.imshow(sourceImage)
        plot.show()


image = Image.open("horse.png")
ShowImage(image)
"""
L: Single channel image (grayscale)
RGB: 3 channel image (colored)
LA: grayscale with alpha channel
RGBA: colored with alpha channel

We can have grayscale image in all modes having "L" or "R=G=B"
Question 1: Should we preserve number of channels for conversions? i.e. RGB->L still 3 channel
Question 2: Should we apply Black&White or colored noises to colored images?
"""

image = ConvertToGrayScale()
ShowImage(image)
image = InvertImage()
ShowImage(image)
image = MirrorImage()
ShowImage(image)
image = AddNoise(var=0.2)
ShowImage(image)
