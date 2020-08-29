from frame import Model, Subject
from . import lane
from . import sign
from . import vehicle
import ui_bridge as ui

def generateForCamera(camera):
    model = {}

    model['sensing'] = Model()
    model['sensing'].addNode(
        name = "Camera",
        category = "framer",
        node = Subject(
            strategy = camera,
            delay = 0))
    
    model['lane'] = lane.generate(frameShape = camera.frameShape)
    model['sign'] = sign.generate(frameShape = camera.frameShape)    
    model['vehicle'] = vehicle.generate()
 
    model['sensing']("Camera", "framer").addObservers(model['lane'].head, model['sign'].head)
    model['sign']("NMS", "interpreted").addObservers(model['vehicle']("signs", "storage"))
    model['lane']("TotalError", "interpreted").addObservers(model['vehicle']("controlPackager", "control"))

    return model


def toButtonCategories(model):
    categories = ui.Categories()
    
    category = ui.ButtonCategory("toggle")
    category.addButtons(model.category("annotator").keys())
    categories.addCategory("Annotation", category)
    
    category = ui.ButtonCategory("radio")
    category.addButtons(model.category("framer").keys())
    categories.addCategory("Frame", category)

    return categories
