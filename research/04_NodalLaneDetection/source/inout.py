import cv2
import numpy

from .Node import Node
from .MaskEdgeDetector import MaskEdgeDetector
from .TwoLineAverage import TwoLineAverage
from . import segment
from . import frame_distributor
from . import roi
from . import line

class LineOutputNode:
    def __call__(self, lines):
        self.output = line.addLinesToFrame(lines, frame_distributor.frame) 
        
outputNode = LineOutputNode()
twoLineAverageNode = Node(
    strategy = TwoLineAverage(
        frameShape = frame_distributor.grabCaptureFrame().shape,
        insetPercentage = 0.60),
    observers = [outputNode])
edgeSegmentatorNode = Node(
    strategy = segment.EdgeSegmentator(
        distancePrecision = 1,
        angularPrecision = numpy.pi/180,
        minimumThreshold = 40),
    observers = [twoLineAverageNode])
regionOfInterestNode = Node(
    strategy = roi.RegionOfInterest(insetWeight = 0.75),
    observers = [edgeSegmentatorNode])
cannyNode = Node(lambda mask: cv2.Canny(mask, 200, 400), [edgeSegmentatorNode])
labMaskNode = Node(lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 110]), numpy.asarray([255, 255, 255])), [cannyNode])
labNode = Node(lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB), [labMaskNode])

frame_distributor.observers = [labNode]
