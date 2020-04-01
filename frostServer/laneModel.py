import cv2
import numpy

import lane
import frame   

def generateForFrameSubject(subject):
    model = frame.Model(subject)

    model.addFramer('LAB', frame.Node(
        subjects = [],
        strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)))

    model.addFramer('Mask', frame.Node(
        subjects = [model.get('LAB')],
        strategy = lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 110]), numpy.asarray([255, 255, 255]))))

    model.addFramer('Canny', frame.Node(
        subjects = [model.get('Mask')],
        strategy = lambda mask: cv2.Canny(mask, 200, 400)))

    model.addFramer('ROI', frame.Node(
        subjects = [model.get('Canny')],
        strategy = lane.RegionOfInterest(insetWeight = 0.75)))

    model.addAnnotator('Segment', frame.Node(
        subjects = [model.get('ROI')],
        strategy = lane.EdgeSegmentator(
            distancePrecision = 1,
            angularPrecision = numpy.pi/180,
            minimumThreshold = 40)))

    model.addAnnotator('Lane', frame.Node(
        subjects = [model.get('Segment')],
        strategy = lane.TwoLineAverage(
            frameShape = subject.frameShape,
            insetPercentage = 0.60)))
    
    model.setHead('LAB')
    return model
