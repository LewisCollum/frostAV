import numpy

class Annotator:
    def __init__(self, frameShape, node, strategy):
        self.frameShape = frameShape
        self.node = node
        self.strategy = strategy

    def __call__(self):
        emptyFrame = numpy.zeros(self.frameShape)
        annotatedFrame = self.strategy(emptyFrame, self.node.output)
        return annotatedFrame
