import cv2
import numpy

clahe = cv2.createCLAHE(tileGridSize=(2,2), clipLimit=15.0)

def execute(image):
    resultImage = clahe.apply(image.astype(numpy.uint8))
    return numpy.reshape(resultImage, (32, 32, 1))
