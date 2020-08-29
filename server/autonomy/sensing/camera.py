import cv2
        
class Camera():
    def __init__(self, source):
        self.capture = cv2.VideoCapture(source)
 
    @property
    def frameShape(self):
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        channels = 3
        return (height, width, channels)

    def __call__(self):
        hasFrame, frame = self.capture.read()
        if hasFrame:
            return frame
