import cv2

from scipy import ndimage
import numpy as np
from PIL import ImageEnhance, Image
from scipy.stats.mstats import mquantiles

def openImage(image_path):
    return cv2.imread(image_path) 

def flipImageAroundX(image):
    """Flip the image around the x axis.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Flipped image
    """
    # Flip the image using cv2.flip() method with parameters image and 0 to flip vertically

    return cv2.flip(image, 0)

def flipImageAroundY(image):
    """Flip the image around the y axis.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Flipped image
    """
    # Flip the image using cv2.flip() method with parameters image and 0 to flip vertically

    return cv2.flip(image, 1)


def gaussianBlurImage(image):
    """Blur the image with gaussian blur.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    return cv2.GaussianBlur(image, (7,7), 10)

def gaussianBlurImage(image):
    """Blur the image with gaussian blur.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    return cv2.GaussianBlur(image, (7,7), 0)

def averagingBlurImage(image):
    """Blur the image with averaging filter.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    return cv2.blur(image,(7,7))

def medianBlurImage(image):
    """Blur the image with median filter.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Blurred image
    """
    return cv2.medianBlur(image, 7)

def deblurImage(image):
    """Deblur image using laplacian filter.

    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: Deblurred image
    """

    kernel = np.array([[0,-1, 0], [-1, 5, -1], [0, -1, 0]]) # laplacian filter
    deblurred_image = cv2.filter2D(image, -1, kernel)
    return deblurred_image

def rotateImage(image, angle):
    """Rotate image by angle

    Args:
        image (numpy.ndarray)
        angle (float): rotation angle in degree

    Returns:
        (numpy.ndarray): Rotated image
    """
    
    rotated_image = ndimage.rotate(image, angle)
    return rotated_image


def changeColorBalance(image, saturationLevel=0.01):
    """The color cast can be removed from an image 
    by scaling the histograms of each of the R, G, and B channels 
    so that they span the complete 0-255 scale. 
    Resource: https://web.stanford.edu/~sujason/ColorBalancing/simplestcb.html
    Args:
        image (numpy.ndarray)

    Returns:
        numpy.ndarray: color balanced image
    """
  
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

    return output_image

def adjustContrast(image, factor):
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
    image = Image.fromarray(np.uint8(image))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor)
    return image

def detectEdges(image, threshold1=100, threshold2=200, L2gradient = False):
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
    edges = cv2.Canny(image, threshold1 = threshold1, threshold2 = threshold2, L2gradient = L2gradient)
    return edges

def saveImage(image, path):
    """It saves images given path

    Args:
        image (numpy.ndarray)
        path (str): path of the image
    """
    cv2.imwrite(path, image)

image_path = "Sharbat-Gula,-the-Afghan-Girl.jpg"
image = cv2.imread(image_path)
cv2.imwrite('flipImageAroundX.jpg', flipImageAroundX(image))
cv2.imwrite('flipImageAroundY.jpg', flipImageAroundY(image))
cv2.imwrite('gaussianBlurImage.jpg', gaussianBlurImage(image))
cv2.imwrite('medianBlurImage.jpg', medianBlurImage(image))
cv2.imwrite('averagingBlurImage.jpg', averagingBlurImage(image))
cv2.imwrite('deblurImage.jpg', deblurImage(image))
cv2.imwrite('rotateImage.jpg', rotateImage(image, 45))
cv2.imwrite('changeColorBalance.jpg', changeColorBalance(image, 0.5))
cv2.imwrite('adjustContrast.jpg', np.asarray(adjustContrast(image, 1)))
cv2.imwrite('adjustContrast.jpg', detectEdges(image, 0.5))