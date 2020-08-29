import cv2
import numpy
import time

from autonomy import lane
from frame import Node, Model, Annotator, Joiner, Packager


def generate(frameShape):
    model = Model()

    addPreprocessingNodes(model, frameShape)
    addPreprocessingAnnotators(model)
    
    addInterpretationNodes(model, frameShape)
    addInterpretationAnnotators(model)    
    
    return model


def addPreprocessingNodes(model, frameShape):
    model.addNode(
        name = "LAB",
        category = "framer",        
        node = Node(
            subject = None,
            strategy = lambda frame: cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)))

    model.addNode(
        name = "Mask",
        category = "framer",        
        node = Node(
            subject = model.previous,
            strategy = lambda frame: cv2.inRange(
                frame,
                numpy.asarray([0, 0, 95]),
                numpy.asarray([255, 255, 255]))))

    model.addNode(
        name = "Blur",
        category = "framer",
        node = Node(
            subject = model.previous,
            strategy = lambda frame: cv2.medianBlur(frame,15)))
    
    model.addNode(
        name = "Canny",
        category = "framer",
        node = Node(
            subject = model.previous,
            strategy = lambda mask: cv2.Canny(mask, 200, 400)))

    model.addNode(
        name = "ROI",
        category = "framer",
        node = Node(
            subject = model.previous,
            strategy = lane.RegionOfInterest(
                insetWeight = 0.75,
                liftWeight = 0.4,
                shallowWeight = 0.6)))
    
    model.addNode(
        name = "Segment",
        category = "geometry",
        node = Node(
            subject = model.previous,
            strategy = lane.HoughLines(
                threshold = 60,
                minLineLength=30,
                maxLineGap=20)))
    
    model.addNode(
        name = "Lane",
        category = "geometry",
        node = Node(
            subject = model.previous,
            strategy = lane.TwoLineAverage(
                frameShape = frameShape,
                insetPercentage = 0.55)))
    
    
def addInterpretationNodes(model, frameShape):
    model.addNode(
        name = "LaneState",
        category = "interpreted",
        node = Packager(
            name = "LaneState",
            node = Node(
                subject = model("Lane", "geometry"),
                strategy = lane.state.fromLines)))

    model.addNode(
        name = "TurnAngle",
        category = "interpreted",
        node = Packager(
            name = "TurnAngle",
            node = Node(
                subject = model("Lane", "geometry"),
                strategy = lane.angle.fromLines)))
    
    model.addNode(
        name = "CrossTrackAngle",
        category = "interpreted",
        node = Packager(
            name = "CrossTrackAngle",
            node = Node(
                subject = model("Lane", "geometry"), 
                strategy = lane.angle.CrossTrackAngle(frameShape))))
    
    model.addNode(
        name = "TurnError",
        category = "interpreted",
        node = Joiner(
            subjectMap = {
                "LaneState": model("LaneState", "interpreted"),
                "TurnAngle": model("TurnAngle", "interpreted")},
            strategy = lane.Error(
                stateNodeName = "LaneState",
                anglesNodeName = "TurnAngle",
                perspectiveAngle = 65)))
    
    model.addNode(
        name = "CrossTrackError",
        category = "interpreted",
        node = Joiner(
            subjectMap = {
                "LaneState": model("LaneState", "interpreted"),
                "CrossTrackAngle": model("CrossTrackAngle", "interpreted")},
            strategy = lane.Error(
                stateNodeName = "LaneState",
                anglesNodeName = "CrossTrackAngle",
                perspectiveAngle = 15)))

    model.addNode(
        name = "SmoothTurnError",
        category = "interpreted",
        node = Packager(
            name = "SmoothTurnError",            
            node = Node(
                subject = model("TurnError", "interpreted"),
                strategy = lane.MovingAverage(5))))
    
    model.addNode(
        name = "SmoothTurnError",
        category = "annotator",
        node = Annotator(
            node = model.previous,
            strategy = lane.annotation.Error(
                label = "Turn Error",
                yWeight = 0.3,
                maxError = 60)))
    
    model.addNode(
        name = "SmoothCrossTrackError",
        category = "interpreted",
        node = Packager(
            name = "SmoothCrossTrackError",
            node = Node(
                subject = model("CrossTrackError", "interpreted"),
                strategy = lane.MovingAverage(5))))

    model.addNode(
        name = "TotalError",
        category = "interpreted",
        node = Joiner(
            subjectMap = {
                "SmoothTurnError": model("SmoothTurnError", "interpreted"),
                "SmoothCrossTrackError": model("SmoothCrossTrackError", "interpreted")},
            strategy = lambda errors: errors["SmoothTurnError"] + errors["SmoothCrossTrackError"]))
    

def addPreprocessingAnnotators(model):
    model.addNode(
        name = "Segment",
        category = "annotator",
        node = Annotator(
            node = model("Segment", "geometry"),
            strategy = lane.annotation.frameLines))

    model.addNode(
        name = "Lane",
        category = "annotator",
        node = Annotator(
            node = model("Lane", "geometry"),
            strategy = lane.annotation.frameLines))
            
def addInterpretationAnnotators(model):
    model.addNode(
        name = "LaneState",
        category = "annotator",
        node = Annotator(
            node = model("LaneState", "interpreted"),
            strategy = lane.annotation.State(yWeight = 0.2)))

    model.addNode(
        name = "CTE",
        category = "annotator",
        node = Annotator(
            node = model("SmoothCrossTrackError", "interpreted"),
            strategy = lane.annotation.Error(
                label = "Cross Track Error",
                yWeight = 0.4,
                maxError = 60)))
    
    model.addNode(
        name = "TotalError",
        category = "annotator",
        node = Annotator(
            node = model("TotalError", "interpreted"),
            strategy = lane.annotation.Error(
                label = "Total Error",
                yWeight = 0.5,
                maxError = 60)))
