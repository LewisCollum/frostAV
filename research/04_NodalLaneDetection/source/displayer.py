import cv2
import frame_distributor
import numpy
totalDisplayers = 0

class Displayer:
    def __init__(self):
        global totalDisplayers
        self.imageName = totalDisplayers
        totalDisplayers += 1
    
    def __call__(self, frame):
        cv2.imshow(f"{self.imageName}", frame)


class LineDisplayer:
    def __init__(self):
        global totalDisplayers
        self.imageName = totalDisplayers
        totalDisplayers += 1
        
    def __call__(self, lines):
        frame = frame_distributor.frame
        lineFrame = numpy.zeros_like(frame)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(lineFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
        lineFrame = cv2.addWeighted(frame, 0.8, lineFrame, 1, 1)
        cv2.imshow(f"{self.imageName}", lineFrame)
