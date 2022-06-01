from . import lane
from . import sign
from . import vehicle
from ..nodal import Model, Subject
from .. import ui_bridge as ui
from .. import nodal_frost

class Frost:
    def __init__(self, camera):
        models = {}

        models['sensing'] = Model()
        models['sensing'].addNode(
            name = "Camera",
            category = "framer",
            node = Subject(
                strategy = camera,
                delay = 0))
    
        models['lane'] = lane.generate(frameShape = camera.frameShape)
        models['sign'] = sign.generate(frameShape = camera.frameShape)    
        models['vehicle'] = vehicle.generate()
    
        models['sensing']("Camera", "framer").addObservers(models['lane'].head, models['sign'].head)
        models['sign']("NMS", "interpreted").addObservers(models['vehicle']("signs", "storage"))
        models['lane']("TotalError", "interpreted").addObservers(models['vehicle']("controlPackager", "control"))
    
        self.models = models
        self.imager = nodal_frost.Imager(defaultSubject = self.models['sensing']("Camera", "framer"))

        
    def start(self):
        self.models['sensing']("Camera", "framer").start()        

    def updateController(self, update):
        self.models['vehicle']("controller", "control")(update)
        
    def updateImager(self, frame, annotators):
        self.imager.annotatorNodes = []

        for model in self.models.values():
            if frame in model.category("framer"):
                self.imager.subject = model(frame, "framer")
                break

        for annotator in annotators:
            for model in self.models.values():            
                if annotator in model.category("annotator"):
                    self.imager.annotatorNodes.append(model(annotator, "annotator"))
        
        
    def generateButtonCategories(self):
        categories = ui.Categories()
        for model in self.models.values():
            categories += toButtonCategories(model)
            
        categories["Frame"].addDefaults(["Camera"])
        return categories



def toButtonCategories(model):
    categories = ui.Categories()

    category = ui.ButtonCategory("toggle")
    category.addButtons(model.category("annotator").keys())
    categories.addCategory("Annotation", category)
    
    category = ui.ButtonCategory("radio")
    category.addButtons(model.category("framer").keys())
    categories.addCategory("Frame", category)

    return categories
