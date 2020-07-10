import cv2
import numpy

from frame import Node, Switchable, Model, Annotator, Timer
import sign
    
def generate(subject):
    model = Model()

    model.add(Node(
        name = 'Blob',
        subjects = [],
        strategy = lambda frame: cv2.dnn.blobFromImage(
            image = frame,
            scalefactor = 1/255,
            size = (416, 416),
            mean = [0,0,0],
            swapRB = True,
            crop = False)))

    model.add(Timer(Node(
        name = 'netTimer',
        subjects = [],
        strategy = lambda delay: (f'Sign FPS: {1/delay:.2f}'))))

    
    model['Blob'].addObservers(model['netTimer'])        

    model.add(Node(
        name = 'Net',
        subjects = [model['Blob']],
        strategy = sign.Net(sign.makeCpuDarknet(
            rootPath = 'sign/yolov3-tiny-prn'))))

    model['Net'].addObservers(model['netTimer'])
    model['netTimer'].addObservers(lambda message: print(message))

    model.addAnnotator(Annotator(
        name = 'NetTimer',
        node = model['netTimer'],
        strategy = sign.label))

    
    model.add(Node(
        name = 'NMS',
        subjects = [model['Net']],
        strategy = sign.DetectionBoxes(
            frameShape = subject.frameShape,
            confidenceThreshold = 0.1,
            nonMaxSuppressionThreshold = 0.2)))
    
    model.addAnnotator(Annotator(
        name = 'Signs',
        node = model['NMS'],
        strategy = sign.DrawDetectionBoxes(
            classes = sign.readClasses("sign/sign.names"))))

    model.setHead('Blob')
    return model
