""" preprocessing """
import cv2
import numpy as np

def grayscale(image):
    """ noise removal """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def noise_removal(image):
    """ noise removal """
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

def preprocess_img(image):
    """ preprocess image """
    image = np.array(image)
    gray_image = grayscale(image)
    thresh, im_bw = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return noise_removal(im_bw)