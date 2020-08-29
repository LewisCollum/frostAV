import numpy
from .line import Line, LaneRegion

class TwoLineAverage:
    def __init__(self, frameShape, insetPercentage):
        self.height, width, _ = frameShape
        self.leftBoundary = width * (1-insetPercentage)
        self.rightBoundary = width * insetPercentage

    def __call__(self, lines):
        leftLines = []
        rightLines = []

        for line in lines:
            x1, y1, x2, y2 = line
            top = (x1, y1) if y1 < y2 else (x2, y2)
            bottom = (x1, y1) if y1 > y2 else (x2, y2)
            dx = bottom[0] - top[0]
            dy = bottom[1] - top[1]
            topToFrameBottom = self.height - top[1]
            bottomXIntersept = topToFrameBottom/dy * dx + top[0]

            line = Line(
                x1=bottomXIntersept,
                y1=self.height,
                x2=top[0],
                y2=top[1])
            
            if bottomXIntersept <= self.leftBoundary:
                leftLines.append(line)
            if bottomXIntersept >= self.rightBoundary:
                rightLines.append(line)

        return LaneRegion(
            left = self.lineAverage(leftLines),
            right = self.lineAverage(rightLines))

    def lineAverage(self, lines):
        if len(lines) > 0: return Line(*numpy.mean(lines, axis=0).astype(int))
        else: return None
