import cv2
import numpy
import frame_distributor

class EdgeSegmentator:
    def __init__(self, distancePrecision, angularPrecision, minimumThreshold):
        self.distancePrecision = distancePrecision
        self.angularPrecision = angularPrecision
        self.minimumThreshold = minimumThreshold
        
    def __call__(self, frame):
        return cv2.HoughLinesP(
            frame,
            self.distancePrecision,
            self.angularPrecision,
            self.minimumThreshold,
            numpy.array([]),
            minLineLength=8,
            maxLineGap=4)

def segmentsToImage(segments):
    frame = frame_distributor.frame
    segmentFrame = numpy.zeros_like(frame)
    
    for segment in segments:
        x1, y1, x2, y2 = segment[0]
        dy = y2-y1
        dx = x2-x1
        r = numpy.sqrt(dy**2 + dx**2)
        theta = numpy.pi/2 if dx == 0 else numpy.arctan(dy/dx)
        cv2.line(segmentFrame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    segmentFrame = cv2.addWeighted(frame, 0.8, segmentFrame, 1, 1)
    return segmentFrame
