import cv2
import numpy
import time

from frame import Node, Switchable, Model, Annotator
import sign

class Timer:
    initialTime = None
    def __init__(self, strategy):
        self.strategy = strategy

    def __call__(self, unused):
        if self.initialTime:
            self.strategy(time.time() - self.initialTime)
            self.initialTime = None
        else:
            self.initialTime = time.time()
            
    
def generateForFrameSubject(subject):
    model = Model()

    model.add('Blob', Node(
        subjects = [],
        strategy = lambda frame: cv2.dnn.blobFromImage(
            image = frame,
            scalefactor = 1/255,
            size = (416, 416),
            mean = [0,0,0],
            swapRB = True,
            crop = False)))

    netTimer = Timer(strategy = lambda delay: print((f'Net Timer: {delay:.2f}s\t'
                                                     f'FPS: {1/delay:.2f}')))
    model.get('Blob').addObservers([netTimer])        

    model.add('Net', Node(
        subjects = [model.get('Blob')],
        strategy = sign.Net(sign.makeCpuDarknet(rootPath = 'sign/my-lite'))))

    model.get('Net').addObservers([netTimer])
        
    model.add('NonMaxSuppression', Node(
        subjects = [model.get('Net')],
        strategy = sign.DetectionBoxes(
            frameShape = subject.frameShape,
            confidenceThreshold = 0.2,
            nonMaxSuppressionThreshold = 0.4)))

    model.addAnnotator('Signs', Annotator(
        frameShape = subject.frameShape,
        node = model.get('NonMaxSuppression'),
        strategy = sign.DrawDetectionBoxes(
            classes = sign.readClasses("sign/sign.names"))))

    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    # t, _ = net.getPerfProfile()
    # label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    # cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    model.setHead('Blob')
    return model






