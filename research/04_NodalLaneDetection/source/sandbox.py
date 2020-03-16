import cv2
import numpy

from Node import Node
import distributor
from MaskEdgeDetector import MaskEdgeDetector
from TwoLineAverage import TwoLineAverage
from WhiteBalancer import WhiteBalancer
import segment
import frame_distributor
from displayer import Displayer, LineDisplayer
import roi

frame_distributor.grabFrame()
    
twoLineAverageNode = Node(
    strategy = TwoLineAverage(
        frameShape = frame_distributor.frame.shape,
        insetPercentage = 0.60),
    observers = [LineDisplayer()])

edgeSegmentatorNode = Node(
    strategy = segment.EdgeSegmentator(
        distancePrecision = 1,
        angularPrecision = numpy.pi/180,
        minimumThreshold = 40),
    observers = [twoLineAverageNode])

regionOfInterestNode = Node(
    strategy = roi.RegionOfInterest(insetWeight = 0.75),
    observers = [edgeSegmentatorNode])

cannyNode = Node(lambda mask: cv2.Canny(mask, 200, 400), [edgeSegmentatorNode, Displayer()])

hsvMaskNode = Node(lambda frame: cv2.inRange(frame, numpy.asarray([100, 50, 110]), numpy.asarray([120, 255, 255])), [cannyNode])
labMaskNode = Node(lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 110]), numpy.asarray([255, 255, 255])), [cannyNode])

labNode = Node(lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB), [Displayer(), labMaskNode])
hsvNode = Node(lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), [Displayer(), hsvMaskNode])
balancerNode = Node(WhiteBalancer(), [labNode])

frame_distributor.startAtHead([labNode])
