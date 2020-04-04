import cv2
import numpy

import lane
import frame   

def generateForFrameSubject(subject):
    model = frame.Model(subject)

    model.addFramer('LAB', frame.Node(
        subjects = [],
        strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)))

    model.addFrameModifier('CLAHE', frame.Node(
        subjects = [model.get('LAB')],
        strategy = lane.Clahe(
            clipLimit = 1000,
            tileGridSize = (4,4),
            frameChannel = 0)))
    
    model.addFramer('Mask', frame.Node(
        subjects = [model.get('CLAHE')],
        strategy = lambda frame: cv2.inRange(frame, numpy.asarray([0, 0, 130]), numpy.asarray([255, 255, 255]))))

    model.addFramer('Canny', frame.Node(
        subjects = [model.get('Mask')],
        strategy = lambda mask: cv2.Canny(mask, 200, 400)))

    model.addFramer('ROI', frame.Node(
        subjects = [model.get('Canny')],
        strategy = lane.RegionOfInterest(
            insetWeight = 0.75,
            liftWeight = 0.2,
            shallowWeight = 0.4)))
    
    model.addAnnotator('Segment', frame.Node(
        subjects = [model.get('ROI')],
        strategy = lambda frame: cv2.HoughLinesP(
            image = frame,
            rho = 1,
            theta = numpy.pi/180,
            threshold = 60,
            minLineLength=10,
            maxLineGap=2)))

    model.addAnnotator('Lane', frame.Node(
        subjects = [model.get('Segment')],
        strategy = lane.TwoLineAverage(
            frameShape = subject.frameShape,
            insetPercentage = 0.60)))

    model.add('CrossTrackError', frame.Node(
        subjects = [model.get('Lane')],
        strategy = lane.CrossTrackError(frameWidth = subject.frameShape[1])))

    # model.add('DisplayCTE', frame.Node(
    #     subjects = [model.get('CrossTrackError')],
    #     strategy = lambda cte: print(cte)))
    
    model.setHead('LAB')
    return model
