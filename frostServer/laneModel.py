import cv2
import numpy
import time

import lane

from frame import Node, Switchable, Model, Annotator, Joiner, Packager
import frame.node as node

def generate(subject):
    model = Model()
    
    model.addFramer(Node(
        name = 'LAB',
        subjects = [],
        strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)))

    model.addFramer(Node(
        name = 'Mask',
        subjects = [model['LAB']],
        strategy = lambda frame: cv2.inRange(
            frame,
            numpy.asarray([0, 0, 95]),
            numpy.asarray([255, 255, 255]))))

    model.addFramer(Node(
        name = 'Blur',
        subjects = [model['Mask']],
        strategy = lambda frame: cv2.medianBlur(frame,15)))
    
    model.addFramer(Node(
        name = 'Canny',
        subjects = [model['Blur']],
        strategy = lambda mask: cv2.Canny(mask, 200, 400)))

    model.addFramer(Node(
        name = 'ROI',
        subjects = [model['Canny']],
        strategy = lane.RegionOfInterest(
            insetWeight = 0.75,
            liftWeight = 0.4,
            shallowWeight = 0.6)))
    
    model.add(Node(
        name = 'Segment',
        subjects = [model['ROI']],
        strategy = lane.HoughLines(
            threshold = 60,
            minLineLength=30,
            maxLineGap=20)))
    
    model.add(Node(
        name = 'Lane',
        subjects = [model['Segment']],
        strategy = lane.TwoLineAverage(
            frameShape = subject.frameShape,
            insetPercentage = 0.55)))


    model.add(Packager(Node(
        name = 'LaneState',
        subjects = [model['Lane']],
        strategy = lane.state.fromLines)))
    model.add(Packager(Node(
        name = 'TurnAngle',
        subjects = [model['Lane']],
        strategy = lane.angle.fromLines)))
    model.add(Packager(Node(
        name = 'CrossTrackAngle',
        subjects = [model['Lane']], 
        strategy = lane.angle.CrossTrackAngle(subject.frameShape))))

    # model.add(Joiner(
    #     name = 'Error',
    #     subjects = [model['LaneState'], model['TurnAngle'], model['CrossTrackAngle']],
    #     strategy = lane.CrossTurnError(
    #         stateNodeName = 'LaneState',
    #         turnAnglesNodeName = 'TurnAngle',
    #         crossTrackAngleNodeName = 'CrossTrackAngle',
    #         perspectiveAngle = 65)))  
    
    
    model.add(Joiner(
        name = 'TurnError',
        subjects = [model['LaneState'], model['TurnAngle']],
        strategy = lane.Error(
            stateNodeName = 'LaneState',
            anglesNodeName = 'TurnAngle',
            perspectiveAngle = 65)))

    model.add(Joiner(
        name = 'CrossTrackError',
        subjects = [model['LaneState'], model['CrossTrackAngle']],
        strategy = lane.Error(
            stateNodeName = 'LaneState',
            anglesNodeName = 'CrossTrackAngle',
            perspectiveAngle = 15)))

    model.add(Packager(Node(
        name = 'SmoothTurnError',
        subjects = [model['TurnError']],
        strategy = lane.MovingAverage(5))))
    model.add(Packager(Node(
        name = 'SmoothCrossTrackError',
        subjects = [model['CrossTrackError']],
        strategy = lane.MovingAverage(5))))

    model.add(Joiner(
        name = 'TotalError',
        subjects = [model['SmoothTurnError'], model['SmoothCrossTrackError']],
        strategy = lambda errors: errors['SmoothTurnError'] + errors['SmoothCrossTrackError']))


    model.addAnnotator(Annotator(
        name = 'Segment',
        node = model['Segment'],
        strategy = lane.annotation.frameLines))
        
    model.addAnnotator(Annotator(
        name = 'Lane',
        node = model['Lane'],
        strategy = lane.annotation.frameLines))
    
    model.addAnnotator(Annotator(
        name = 'TurnError',
        node = model['SmoothTurnError'],
        strategy = lane.annotation.Error(
            label = 'Turn Error',
            yWeight = 0.3,
            maxError = 60)))
    
    model.addAnnotator(Annotator(
        name = 'CTE',
        node = model['SmoothCrossTrackError'],
        strategy = lane.annotation.Error(
            label = 'Cross Track Error',
            yWeight = 0.4,
            maxError = 60)))
    
    model.addAnnotator(Annotator(
        name = 'TotalError',
        node = model['TotalError'],
        strategy = lane.annotation.Error(
            label = 'Total Error',
            yWeight = 0.5,
            maxError = 60)))

    # model.addAnnotator(Annotator(
    #     name = 'Error',
    #     node = model['Error'],
    #     strategy = lane.annotation.Error(
    #         label = 'Error',
    #         yWeight = 0.5,
    #         maxError = 60)))    
    
    model.addAnnotator(Annotator(
        name = 'LaneState',
        node = model['LaneState'],
        strategy = lane.annotation.State(
            yWeight = 0.2)))

    # node.addObserverToSubjects(print, [
    #     model['TurnError'],
    #     model['CrossTrackError']])
    
    model['Lane']
    model.setHead('LAB')
    return model
