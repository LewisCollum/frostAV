import cv2
import numpy
import time

from frame import Node, Switchable, Model, Annotator
import sign

class Timer:
    initialTime = None
    def __init__(self, node):
        self.node = node

    @property
    def name(self):
        return self.node.name

    def addObservers(self, observers):
        self.node.addObservers(observers)
        
    def __call__(self, unused):
        if self.initialTime:
            self.node(time.time() - self.initialTime)
            self.initialTime = None
        else:
            self.initialTime = time.time()

    def pull(self):
        return self.node.pull()

    
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

    
    model['Blob'].addObservers([model['netTimer']])        

    model.add(Node(
        name = 'Net',
        subjects = [model['Blob']],
        strategy = sign.Net(sign.makeCpuDarknet(
            rootPath = 'sign/yolov3-tiny-prn'))))

    model['Net'].addObservers([model['netTimer']])

    model['netTimer'].addObservers([
        lambda message: print(message)])


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

    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    # t, _ = net.getPerfProfile()
    # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    model.setHead('Blob')
    return model






