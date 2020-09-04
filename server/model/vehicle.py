import cv2
import numpy

from nodal import Node, Model, Annotator
from autonomy import vic

from collections import deque
class Signs:
    def __init__(self, maxSigns):
        self.signs = deque(maxlen = maxSigns)

    def __call__(self, sign):
        if sign:
            self.signs.append(sign)
            # print('Sign Added')
        else:
            # print('popped')
            if not self.isEmpty():
                self.signs.pop()

    def isEmpty(self):
        return len(self.signs) == 0
        
    def pull(self):
        return self.signs.pop()

    
def generate():
    model = Model()

    model.addNode(
        name = "signs",
        category = "storage",
        node = Node(
            subject = None,
            strategy = Signs(maxSigns = 1)))    
    
    model.addNode(
        name = "controlPackager",
        category = "control",
        node = Node(
            subject = None,
            strategy = lambda error: {
                'steering': error,
                'forward': 5 if model("signs", "storage").strategy.isEmpty() else 0,
                'reverse': 0}))
        
    model.addNode(
        name = "controller",
        category = "control",
        node = Node(
            subject = model("controlPackager", "control"),
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
