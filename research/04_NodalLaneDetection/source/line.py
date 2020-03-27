import cv2
import numpy

def addLinesToFrame(lines, frame):
    lineFrame = numpy.zeros_like(frame)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(lineFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
    lineFrame = cv2.addWeighted(frame, 0.8, lineFrame, 1, 1)    
    return lineFrame
