import numpy

class Annotator:
    def __init__(self, node, strategy):
        self.node = node
        self.strategy = strategy
                
    def __call__(self, frame):
        annotatedFrame = self.strategy(frame, self.node.pull())
        return annotatedFrame
