from collections import deque
import numpy

class MovingAverage:
    def __init__(self, sampleSize):
        self.sampleSize = sampleSize
        self.samples = deque(maxlen = sampleSize)

    def __call__(self, value):
        self.samples.append(value)
        return numpy.mean(self.samples)
