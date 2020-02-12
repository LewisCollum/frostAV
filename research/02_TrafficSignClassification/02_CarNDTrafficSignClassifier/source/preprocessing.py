import cv2
import numpy

clahe = cv2.createCLAHE(tileGridSize=(2,2), clipLimit=15.0)

def execute(image):
    return numpy.reshape(clahe.apply(image.astype(numpy.uint8)).astype(numpy.float64), (32, 32, 1))
