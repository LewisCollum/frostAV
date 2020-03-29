import cv2
import numpy

class EdgeSegmentator:
    def __init__(self, distancePrecision, angularPrecision, minimumThreshold):
        self.distancePrecision = distancePrecision
        self.angularPrecision = angularPrecision
        self.minimumThreshold = minimumThreshold
        
    def __call__(self, frame):
        return cv2.HoughLinesP(
            frame,
            self.distancePrecision,
            self.angularPrecision,
            self.minimumThreshold,
            numpy.array([]),
            minLineLength=8,
            maxLineGap=4)
