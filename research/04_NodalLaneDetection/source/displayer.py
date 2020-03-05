import cv2

class Displayer:
    totalDisplayers = 0

    def __init__(self):
        self.id = self.totalDisplayers
        self.totalDisplayers += 1
    
    def __call__(self, frame):
        cv2.imshow(f"{self.id}", frame)
