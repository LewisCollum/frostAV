import cv2
import numpy

def addLines(frame, lines):
    lineFrame = numpy.zeros_like(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(
                img = lineFrame,
                pt1 = (x1, y1),
                pt2 = (x2, y2),
                color = (0, 255, 0),
                thickness = 2)
        
    return lineFrame
