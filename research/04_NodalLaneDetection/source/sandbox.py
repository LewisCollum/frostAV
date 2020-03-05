import cv2
import numpy

from Node import Node
import distributor
from MaskEdgeDetector import MaskEdgeDetector
import segment
import frame_distributor
from displayer import Displayer
import roi

def displayAsVectors(frame): print(frame)

def slope(segments):
    print(numpy.mean(segments, 0))
    for segment in segments:
        x1, y1, x2, y2 = segment[0]
        dy = y2-y1
        dx = x2-x1
        r = numpy.sqrt(dy**2 + dx**2)
        theta = numpy.pi/2 if dx == 0 else numpy.arctan(dy/dx)
        print(segment[0])
        print(r, theta)

def meanSegmentSlope(segments):
    for segment in segments:
        x1, y1, x2, y2 = segment[0]
        #...


segmentImage = Node(
    strategy = segment.segmentsToImage,
    distributor = distributor.SingleDistributor(Displayer()))

segmentSlopeAverager = Node(
    strategy = meanSegmentSlope,
    distributor = distributor.MultiDistributor([]))

edgeSegmentator = Node(
    strategy = segment.EdgeSegmentator(
        distancePrecision = 1,
        angularPrecision = numpy.pi/180,
        minimumThreshold = 80),
    distributor = distributor.MultiDistributor([segmentImage, slope, segmentSlopeAverager]))

regionOfInterest = Node(
    strategy = roi.RegionOfInterest(insetWeight = 0.75),
    distributor = distributor.MultiDistributor([Displayer(), edgeSegmentator]))

edgeDetector = Node(
    strategy = MaskEdgeDetector(
        maskLower = numpy.asarray([60, 40, 40]),
        maskUpper = numpy.asarray([150, 255, 255])),
    distributor = distributor.MultiDistributor([Displayer(), regionOfInterest]))



frame_distributor.startAtHead(edgeDetector)
