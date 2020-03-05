import cv2

class MaskEdgeDetector:
    def __init__(self, maskLower, maskUpper):
        self.maskLower = maskLower
        self.maskUpper = maskUpper

    def __call__(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.maskLower, self.maskUpper)
        edges = cv2.Canny(mask, 200, 400)
        return edges
