import cv2
import numpy

from frame import Node, Switchable, Model, Annotator, Timer
import sign
    
def generate(frameShape):
    model = Model()

    model.addNode(
        name = "Blob",
        category = "preprocessing",
        node = Node(
            subject = None,
            strategy = lambda frame: cv2.dnn.blobFromImage(
                image = frame,
                scalefactor = 1/255,
                size = (416, 416),
                mean = [0,0,0],
                swapRB = True,
                crop = False)))

    model.addNode(
        name = "NetTimer",
        category = "logging",
        node = Timer(Node(
            subject = None,
            strategy = lambda delay: (f'Sign FPS: {1/delay:.2f}'))))

    
    model("Blob", "preprocessing").addObservers(model("NetTimer", "logging"))

    model.addNode(
        name = "Net",
        category = "interpreted",
        node = Node(
            subject = model("Blob", "preprocessing"),
            strategy = sign.Net(sign.makeCpuDarknet(
                rootPath = 'sign/yolov3-tiny-prn'))))

    model("Net", "interpreted").addObservers(model("NetTimer", "logging"))

    model.addNode(
        name = "NetTimer",
        category = "annotator",
        node = Annotator(
            node = model("NetTimer", "logging"),
            strategy = sign.label))

    
    model.addNode(
        name = "NMS",
        category = "interpreted",
        node = Node(
            subject = model("Net", "interpreted"),
            strategy = sign.DetectionBoxes(
                frameShape = frameShape,
                confidenceThreshold = 0.1,
                nonMaxSuppressionThreshold = 0.2)))
    
    model.addNode(
        name = "Signs",
        category = "annotator",
        node = Annotator(
            node = model("NMS", "interpreted"),
            strategy = sign.DrawDetectionBoxes(
                classes = sign.readClasses("sign/sign.names"))))

    return model
