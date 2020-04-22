import cv2

class Clahe:
    def __init__(self, clipLimit, tileGridSize, frameChannel):
        self.clipLimit = clipLimit
        self.tileGridSize = tileGridSize
        self.clahe = cv2.createCLAHE(self.clipLimit, self.tileGridSize)
        self.frameChannel = frameChannel
        
    def __call__(self, frame):
        claheFrame = frame.copy()
        claheFrame[...,self.frameChannel] = self.clahe.apply(claheFrame[...,self.frameChannel])
        return claheFrame

class ClaheGray:
    def __init__(self, clipLimit, tileGridSize):
        self.clipLimit = clipLimit
        self.tileGridSize = tileGridSize
        self.clahe = cv2.createCLAHE(self.clipLimit, self.tileGridSize)
        
    def __call__(self, frame):
        claheFrame = frame.copy()
        claheFrame = self.clahe.apply(claheFrame)
        return claheFrame
    
