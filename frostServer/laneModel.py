import cv2
import numpy

import lane
from frame import Node, Switchable, Model, Annotator
from frame import line

def generateForFrameSubject(subject):
    model = Model()

    model.addFramer('LAB', Node(
        subjects = [],
        strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)))

    model.addSwitchable('CLAHE', Switchable(Node(
        subjects = [model.get('LAB')],
        strategy = lane.Clahe(
            clipLimit = 1000,
            tileGridSize = (4,4),
            frameChannel = 0))))
    
    model.addFramer('Mask', Node(
        subjects = [model.get('CLAHE')],
        strategy = lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 110]), numpy.asarray([255, 255, 255]))))

    model.addFramer('Canny', Node(
        subjects = [model.get('Mask')],
        strategy = lambda mask: cv2.Canny(mask, 200, 400)))

    model.addFramer('ROI', Node(
        subjects = [model.get('Canny')],
        strategy = lane.RegionOfInterest(
            insetWeight = 0.75,
            liftWeight = 0.2,
            shallowWeight = 0.4)))
    
    model.add('Segment', Node(
        subjects = [model.get('ROI')],
        strategy = lambda frame: cv2.HoughLinesP(
            image = frame,
            rho = 1,
            theta = numpy.pi/180,
            threshold = 60,
            minLineLength=10,
            maxLineGap=2)))
    
    model.addAnnotator('Segment', Annotator(
        frameShape = subject.frameShape,
        node = model.get('Segment'),
        strategy = line.addLines))
    
    model.add('Lane', Node(
        subjects = [model.get('Segment')],
        strategy = lane.TwoLineAverage(
            frameShape = subject.frameShape,
            insetPercentage = 0.60)))

    model.addAnnotator('Lane', Annotator(
        frameShape = subject.frameShape,
        node = model.get('Lane'),
        strategy = line.addLines))
    
    model.add('CrossTrackError', Node(
        subjects = [model.get('Lane')],
        strategy = lane.CrossTrackError(frameWidth = subject.frameShape[1])))

    # model.add('DisplayCTE', Node(
    #     subjects = [model.get('CrossTrackError')],
    #     strategy = lambda cte: print(cte)))
    
    model.setHead('LAB')
    return model
