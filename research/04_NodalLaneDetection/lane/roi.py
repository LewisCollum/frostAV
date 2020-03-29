import cv2
import numpy

class RegionOfInterest:
    def __init__(self, insetWeight = 1):
        self.insetWeight = insetWeight
        
    def __call__(self, frame):
        height, width = frame.shape
        mask = numpy.zeros_like(frame)
        
        polygon = numpy.array([[
            (width * self.insetWeight/2, 0),
            (width * (1 - self.insetWeight/2), 0),
            (width, height),
            (0, height),
        ]], numpy.int32)
        
        cv2.fillPoly(mask, polygon, 255)
        frame = cv2.bitwise_and(frame, mask)
        return frame
