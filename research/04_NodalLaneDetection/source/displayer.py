import cv2
import numpy

from . import frame_distributor
from . import line

totalDisplayers = 0

def newImageName():
    global totalDisplayers
    name = totalDisplayers
    totalDisplayers += 1
    return name
    

class Displayer:
    def __init__(self):
        self.imageName = newImageName()
    
    def __call__(self, frame):
        cv2.imshow(f"{self.imageName}", frame)


class LineDisplayer:
    def __init__(self):
        self.image = newImageName()
        
    def __call__(self, lines):
        frame = line.addLinesToFrame(lines, frame_distributor.frame)
        cv2.imshow(f"{self.imageName}", frame)
