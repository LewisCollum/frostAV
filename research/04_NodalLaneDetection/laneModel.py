import cv2
import numpy

import lane
import frame

labNode = lane.Node(
    subjects = [frame.subject],
    strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB))

labMaskNode = lane.Node(
    subjects = [labNode],
    strategy = lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 110]), numpy.asarray([255, 255, 255])))

cannyNode = lane.Node(
    subjects = [labMaskNode],
    strategy = lambda mask: cv2.Canny(mask, 200, 400))

regionOfInterestNode = lane.Node(
    subjects = [cannyNode],
    strategy = lane.RegionOfInterest(insetWeight = 0.75))

edgeSegmentatorNode = lane.Node(
    subjects = [regionOfInterestNode],
    strategy = lane.EdgeSegmentator(
        distancePrecision = 1,
        angularPrecision = numpy.pi/180,
        minimumThreshold = 40))

twoLineAverageNode = lane.Node(
    subjects = [edgeSegmentatorNode],
    strategy = lane.TwoLineAverage(
        frameShape = frame.subject.grabCaptureFrame().shape,
        insetPercentage = 0.60))
