import cv2
import numpy

from .line import addLines
from . import subject

class Displayer:
    def __init__(self):
        self.imageName = newImageName()
    
    def __call__(self, frame):
        cv2.imshow(f"{self.imageName}", frame)


class LineDisplayer:
    def __init__(self):
        self.imageName = newImageName()
        
    def __call__(self, lines):
        frame = addLines(lines)
        cv2.imshow(f"{self.imageName}", frame)

totalDisplayers = 0
def newImageName():
    global totalDisplayers
    name = totalDisplayers
    totalDisplayers += 1
    return name
