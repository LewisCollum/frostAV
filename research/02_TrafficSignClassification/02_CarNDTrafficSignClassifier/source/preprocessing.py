import cv2
import numpy

clahe = cv2.createCLAHE(tileGridSize=(2,2), clipLimit=15.0)

def execute(image):
    resultImage = clahe.apply(image.astype(numpy.uint8))
    return resultImage.reshape(image.shape[0], image.shape[1], 1).astype(numpy.float32)
