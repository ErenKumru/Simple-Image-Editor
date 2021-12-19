# Eren's initial work file
# can create new files when necessary

from matplotlib import pyplot as plot
from PIL import Image, ImageOps, ImageEnhance
from skimage.util import random_noise
import numpy as np


def IsTransparent(sourceImage):
    if(sourceImage.mode == "RGBA" or "transparency" in sourceImage.info):
        return True
    return False


def NumberOfChannels(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3):
        return 1
    return np.asarray(sourceImage).shape[2]


def IsGrayScale(sourceImage):
    if(len(np.asarray(sourceImage).shape) < 3):
        return True
    if(NumberOfChannels(sourceImage) == 1):
        return True

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

    print("ConvertToGrayScale: The source image is converted to grayscale successfully.")
    return image.convert("L")


def InvertImage():
    if(IsTransparent(image)):
        sourceImage = image.convert("RGB")
        print("InvertImage: The transparent source image is inverted successfully.")
        return ImageOps.invert(sourceImage).convert("RGBA")

    print("InvertImage: The source image is inverted successfully.")
    return ImageOps.invert(image)


def MirrorImage():
    print("MirrorImage: The source image is mirrored successfully.")
    return ImageOps.mirror(image)


def AddNoise(mode="gaussian", var=0.0025, amount=0.05):
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

    if(var < 0 or 0.0):
        print("AddNoise: Negative \"var\" value is invalid! No noise added.")
        return image

    if(amount < 0 or 0.0):
        print("AddNoise: Negative \"amount\" value is invalid! No noise added.")
        return image

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
    return Image.fromarray(noiseImage)


# factor = 1 -> original image
# 0 < factor < 1 -> darkened image
# factor > 1 -> brightened image
def AdjustBrightness(factor=1.5):
    if(factor < 0 or 0.0):
        print("AdjustBrightness: Negative \"factor\" value is invalid! Brightness is not modified.")
        return image

    enhancer = ImageEnhance.Brightness(image)
    print("AdjustBrightness: The brightness of the source image is adjusted by a factor of {} successfully.".format(factor))
    return enhancer.enhance(factor)


# factor = 1 -> original image
# 0 < factor < 1-> muted or calmed image
# factor > 1 -> saturated image
def AdjustSaturation(factor=1.75):
    if(factor < 0 or 0.0):
        print("AdjustSaturation: Negative \"factor\" value is invalid! Saturation is not modified.")
        return image

    enhancer = ImageEnhance.Color(image)
    print("AdjustSaturation: The saturation of the source image is adjusted by a factor of {} successfully.".format(factor))
    return enhancer.enhance(factor)


# (left, top) = top left coordinates i.e (x,y)
# (right, bottom) = bottom right coordinates i.e. (x,y)
# Area to be cropped:
#       left <= x < right and top <= y < bottom
def CropImage(left, top, right, bottom):
    if(left >= right or top >= bottom):
        print("CropImage: Invalid positions! Can not crop image from left = {} top = {} to right = {} bottom = {}."
              "\n\t\t   Should satisfy \"right > left and bottom > top\"".format(left, top, right, bottom))
        return image

    if(left < 0):
        left = 0
    if(top < 0):
        top = 0
    if(right > image.size[0]):
        right = image.size[0]
    if(bottom > image.size[1]):
        bottom = image.size[1]

    print("CropImage: The source image is cropped from left = {} top = {} to right = {} bottom = {} successfully.".format(left, top, right, bottom))
    return image.crop((left, top, right, bottom))


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


"""
L: Single channel image (grayscale)
RGB: 3 channel image (colored)
LA: grayscale with alpha channel
RGBA: colored with alpha channel
"""
# Image should be read dynamically from the UI.
image = Image.open("Sharbat Gula, the Afghan Girl.jpg")
ShowImage(image)

if(IsGrayScale(image)):
    image = image.convert("L")

image = AdjustSaturation()
ShowImage(image)
image = InvertImage()
ShowImage(image)
image = ConvertToGrayScale()
ShowImage(image)
image = MirrorImage()
ShowImage(image)
image = AddNoise()
ShowImage(image)
image = AdjustBrightness()
ShowImage(image)
image = CropImage(left=300, top=300, right=1600, bottom=1200)
ShowImage(image)
