import cv2
import numpy

from .line import Line

class HoughLines:
    def __init__(self, threshold, minLineLength, maxLineGap):
        self.threshold = threshold
        self.minLineLength = minLineLength
        self.maxLineGap = maxLineGap
        
    def __call__(self, frame):
        segments = cv2.HoughLinesP(
            image = frame,
            rho = 1,
            theta = numpy.pi/180,
            threshold = self.threshold,
            minLineLength=self.minLineLength,
            maxLineGap=self.maxLineGap)

        lines = []
        if segments is not None:        
            for segment in segments:
                lines.append(Line(
                    x1=segment[0][0],
                    y1=segment[0][1],
                    x2=segment[0][2],
                    y2=segment[0][3]))
                
        return lines
