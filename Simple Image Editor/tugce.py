import cv2

from scipy import ndimage
import numpy as np
from PIL import ImageEnhance, Image, ImageFilter 
from scipy.stats.mstats import mquantiles

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


def openImage(image_path):
    return cv2.imread(image_path) 

def flip(image):
    """Flip the image around the x axis.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Flipped image
    """
    # Flip the image using cv2.flip() method with parameters image and 0 to flip vertically

    return image.transpose(Image.FLIP_TOP_BOTTOM)


def gaussianBlurImage(image):
    """Blur the image with gaussian blur.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    return image.filter(ImageFilter.GaussianBlur(radius = 1))

def deblurImage(image):
    """Deblur image using laplacian filter.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Deblurred image
    """

    return image.filter(ImageFilter.Kernel((3,3), (0, -1, 0, -1, 5, -1, 0, -1, 0)))


def rotateImage(image):
    """Rotate image by angle

    Args:
        image (numpy.ndarray)
        angle (float): rotation angle in degree

    Returns:
        (numpy.ndarray): Rotated image
    """

    return image.rotate(90)


def changeColorBalance(image, saturationLevel=0.5):
    """The color cast can be removed from an image 
    by scaling the histograms of each of the R, G, and B channels 
    so that they span the complete 0-255 scale. 
    Resource: https://web.stanford.edu/~sujason/ColorBalancing/simplestcb.html
    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: color balanced image
    """
    if IsGrayScale(image):
        return image
    
    image = np.asarray(image)
    # 1. Determine the histogram for each RGB channel 
    # find the quantiles that correspond to our desired saturation level.
    # saturationLevel controls the saturation of a certain percentage of the pixels to black and white.
    q = np.array([saturationLevel/2.0, 1 - saturationLevel/2.0]) 

    output_image = np.zeros(image.shape)
    for dim in range(image.shape[2]): # For R, G, B channels in image
        low, high  = mquantiles(image[:, :,dim], q, alphap=0.5, betap=0.5) # alphap and betap are plotting positions parameter
        
        # 2. Cut off the outlying values by saturating a certain percentage of the pixels to black and white.
        # Set pixel value to low where pixel value is smaller than low,
        # Set pixel value to high where pixel value is greater than high
        output_image[:, :,dim] = np.where(image[:, :,dim] < low, low,
                                (np.where(image[:, :,dim] > high, high, image[:, :,dim])))
        
        # 3. Scale the saturated histogram to span the full 0-255 range.
        min = np.amin(output_image[:, :,dim]) # Min value of the channel
        max = np.amax(output_image[:, :,dim]) # Max value of the channel
        difference = (max - min if max - min != 0 else 1) # Difference cannot be equal to 1.
        output_image[:, :, dim] = (output_image[:, :,dim] - min) * 255 / difference
    return Image.fromarray(output_image.astype(np.uint8))

def adjustContrast(image, factor=0.5):
    """Adjust image contrast. 
    An enhancement factor of 0.0 gives a solid grey image. 
    A factor of 1.0 gives the original image.

    Args:
        image ([type]): [description]
        factor (float): Image contrast will change with a factor. 
        If factor is equal to 1, it gives original image.
        If factor is less than 1, image's constrast will be decreased.
        If factor is greater than 1, image's contrast will be increased.
    """
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor)
    return image

def detectEdges(image, threshold1=120, threshold2=150, L2gradient = False):
    """Detect the edges using Canny Algorithm.
    Consists of 4 steps:
        1. Noise reduction
        2. Finding intensity gradient of the image
        3. Finding intensity gradient of the image
        4. Non-maximum suppression
        5. Hystresis Thresholding

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    
    #L2gradient specifies the equation for finding gradient magnitude. Edge_Gradient(G)=|Gx|+|Gy|
    edges = cv2.Canny(np.asarray(image), threshold1 = threshold1, threshold2 = threshold2, L2gradient = L2gradient)
    return Image.fromarray(edges)

def saveImage(image, path):
    """It saves images given path

    Args:
        image (numpy.ndarray)
        path (str): path of the image
    """
    cv2.imwrite(path, image)

image_path = "/home/tugcekizilepe/Desktop/BBM415/Project/Simple-Image-Editor2/Sharbat-Gula,-the-Afghan-Girl.jpg"
image = Image.open(image_path)
flip(image).save('flipImageAroundX.jpg')
gaussianBlurImage(image).save('gaussianBlurImage.jpg')
gaussianImage=gaussianBlurImage(image)
rotateImage(image).save('rotateImage.jpg')
changeColorBalance(image).save('changeColorBalance.jpg')
adjustContrast(image).save('adjustContrast.jpg')
detectEdges(gaussianImage).save('detectEdgesBlurred.jpg')
detectEdges(image).save('detectEdges.jpg')