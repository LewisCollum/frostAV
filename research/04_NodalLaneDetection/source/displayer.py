import cv2

class Displayer:
    totalDisplayers = 0

    def __init__(self):
        self.imageName = Displayer.totalDisplayers
        Displayer.totalDisplayers += 1
    
    def __call__(self, frame):
        cv2.imshow(f"{self.imageName}", frame)
