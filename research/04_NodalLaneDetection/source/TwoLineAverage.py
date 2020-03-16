import numpy
from sklearn.neighbors import KernelDensity

class TwoLineAverage:
    def __init__(self, frameShape, insetPercentage):
        self.height, width, _ = frameShape
        self.leftBoundary = width * (1-insetPercentage)
        self.rightBoundary = width * insetPercentage
        
    def __call__(self, lines):
        lanes = []
        left = []
        right = []
        total = []

        for line in lines:
            x1, y1, x2, y2 = line[0].astype(int)
            top = (x1, y1) if y1 > y2 else (x2, y2)
            bottom = (x1, y1) if y1 < y2 else (x2, y2)
            dx = bottom[0] - top[0]
            dy = bottom[1] - top[1]
            topToFrameBottom = self.height - top[1]
            bottomXIntersept = topToFrameBottom/dy * dx + top[0]
            if bottomXIntersept <= self.leftBoundary:
                left.append(numpy.asarray([bottomXIntersept, *top, *bottom]))
            if bottomXIntersept >= self.rightBoundary:
                right.append(numpy.asarray([bottomXIntersept, *top, *bottom]))

        if len(left) >= 3:
            leftAverage = numpy.mean(left, axis = 0).astype(int)
            lanes.append([[leftAverage[0], self.height, leftAverage[1], leftAverage[2]]])

        if len(right) >= 3:
            rightAverage = numpy.mean(right, axis = 0).astype(int)
            lanes.append([[rightAverage[0], self.height, rightAverage[1], rightAverage[2]]])
            
        return lanes
