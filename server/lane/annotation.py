import numpy
import cv2
from PIL import ImageFont, ImageDraw, Image

class Error:
    def __init__(self, label, yWeight, maxError):
        self.label = label
        self.yWeight = yWeight
        self.maxError = maxError

    def __call__(self, frame, error):
        height, width, _ = frame.shape
        y = int(self.yWeight * height)
        xCenter = int(0.5*width)
        if error is None:
            error = 0
        normalizedError = error/self.maxError
        x = int(-normalizedError * width/2 + xCenter)

        label = f"{self.label}: {round(error)} deg"
        labelOffset = -20
        
        (labelWidth, labelHeight) = cv2.getTextSize(
            text = label,
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.7,
            thickness = 1)[0]
        
        cv2.putText(
            img = frame,
            text = label,
            org = (xCenter - int(labelWidth/2), y + int(labelHeight/2) + labelOffset),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.7,
            color = (0, 255, 255),
            thickness = 1)
        
        cv2.arrowedLine(
            img = frame,
            pt1 = (xCenter, y),
            pt2 = (x, y),
            color = (255, 255, 0),
            thickness = int(abs(normalizedError*5)) + 2)

        return frame    


class State:
    def __init__(self, yWeight):
        self.yWeight = yWeight
        self.stateToDescription = {
            'Lane': 'Both Lines Detected',
            'NoLane': 'No Lines Detected',
            'LeftOnly': 'Left Line Detected',
            'RightOnly': 'Right Line Detected'}
                
    def __call__(self, frame, state):
        height, width, _ = frame.shape
        y = int(self.yWeight * height)
        centerX = int(0.5*width)

        label = self.stateToDescription[state]
        
        (labelWidth, labelHeight) = cv2.getTextSize(
            text = label,
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 1,
            thickness = 2)[0]
        
        cv2.putText(
            img = frame,
            text = label,
            org = (centerX - int(labelWidth/2), y + int(labelHeight/2)),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 1,
            color = (0, 255, 255),
            thickness = 2)
        return frame
        
def frameLines(frame, lines):
    for line in lines:
        if line:
            cv2.line(
                img = frame,
                pt1 = (line.x1, line.y1),
                pt2 = (line.x2, line.y2),
                color = (0, 255, 0),
                thickness = 2)
    return frame
