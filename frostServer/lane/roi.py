import cv2
import numpy

class RegionOfInterest:
    def __init__(self, insetWeight, liftWeight, shallowWeight):
        self.insetWeight = insetWeight
        self.liftWeight = liftWeight
        self.shallowWeight = shallowWeight
        
    def __call__(self, frame):
        height, width = frame.shape
        mask = numpy.zeros_like(frame)
        
        polygon = numpy.array([[
            (width * self.insetWeight/2, height*self.shallowWeight),
            (width * (1 - self.insetWeight/2), height*self.shallowWeight),
            (width, height*(1-self.liftWeight)),
            (width, height),
            (0, height),
            (0, height*(1-self.liftWeight)),
        ]], numpy.int32)
        
        cv2.fillPoly(mask, polygon, 255)
        frame = cv2.bitwise_and(frame, mask)
        return frame
