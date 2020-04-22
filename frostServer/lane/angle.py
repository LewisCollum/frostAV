import numpy

from .line import LaneRegion

def angleOfLine(line):
    dy = abs(line.y2 - line.y1)
    dx = abs(line.x2 - line.x1)
    return numpy.rad2deg(numpy.arctan(dy/dx)) if dx != 0 else 90

def fromLines(laneLines):
    return LaneRegion(
        left = angleOfLine(laneLines.left) if laneLines.left is not None else None,
        right = angleOfLine(laneLines.right) if laneLines.right is not None else None)

class CrossTrackAngle:
    def __init__(self, frameShape):
        self.height, self.width, _ = frameShape
        self.xCenter = self.width/2
        
    def __call__(self, laneLines):

        if laneLines.left:
            leftAngle = numpy.rad2deg(numpy.arctan((laneLines.left.x1 - self.xCenter)/self.height))
        if laneLines.right:
            rightAngle = numpy.rad2deg(numpy.arctan((self.xCenter - laneLines.right.x1)/self.height))

        return LaneRegion(
            left = -leftAngle if laneLines.left is not None else None,
            right = -rightAngle if laneLines.right is not None else None)
    
    
    
