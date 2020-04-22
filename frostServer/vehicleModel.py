import cv2
import numpy

from frame import Node, Switchable, Model, Annotator
import vic

from collections import deque
class Signs:
    def __init__(self, maxSigns):
        self.signs = deque(maxlen = maxSigns)

    def __call__(self, sign):
        if sign:
            self.signs.append(sign)
            print('Sign Added')
        else:
            print('popped')
            if not self.isEmpty():
                self.signs.pop()

    def isEmpty(self):
        return len(self.signs) == 0
        
    def pull(self):
        return self.signs.pop()

    
def generate():
    model = Model()

    model.add(Node(
        name = 'signs',
        subjects = [],
        strategy = Signs(maxSigns = 1)))    
    
    model.add(Node(
        name = 'controlPackager',
        subjects = [],
        strategy = lambda error: {'steering': error, 'forward': 5 if model['signs'].strategy.isEmpty() else 0, 'reverse': 0}))
    
    model.add(Node(
        name = 'controller',
        subjects = [model['controlPackager']],
        strategy = vic.VehicleInterfaceController()))
    
    # model.add(Node(
    #     name = 'driveController',
    #     subjects = [],
    #     strategy = lambda error: None))
    
    # model.add(Node(
    #     name = 'steeringController',
    #     subjects = [],
    #     strategy = lambda error: None))
            
    return model
