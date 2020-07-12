import cv2

class MaskEdgeDetector:
    def __init__(self, maskLower, maskUpper):
        self.maskLower = maskLower
        self.maskUpper = maskUpper

    def __call__(self, frame):
        mask = cv2.inRange(frame, self.maskLower, self.maskUpper)
        edges = cv2.Canny(mask, 200, 400)
        return edges

class HsvMaskEdgeDetector:
    def __init__(self, maskLower, maskUpper):
        self.maskLower = maskLower
        self.maskUpper = maskUpper

    def __call__(self, frame):
        mask = cv2.inRange(frame, self.maskLower, self.maskUpper)
        edges = cv2.Canny(mask, 200, 400)
        return edges
