import numpy

class Annotator:
    def __init__(self, name, node, strategy):
        self.name = name
        self.node = node
        self.strategy = strategy
                
    def __call__(self, frame):
        annotatedFrame = self.strategy(frame, self.node.pull())
        return annotatedFrame
