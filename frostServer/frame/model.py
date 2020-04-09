from .switchable import Switchables

class Model:
    def __init__(self):
        self.model = {}
        self.framers = []
        self.switchables = Switchables()
        self.annotators = {}        
        self.headName = None

    def setHead(self, headName):
        self.headName = headName

    @property
    def head(self): return self.get(self.headName)
        
    def add(self, name, node):
        self.model[name] = node
        
    def addFramer(self, name, node):
        self.add(name, node)
        self.framers.append(name)

    def addSwitchable(self, name, node):
        self.add(name, node)
        self.switchables.add(name, node)

    def addAnnotator(self, name, annotator):
        self.annotators[name] = annotator
        
    def get(self, name):
        return self.model[name]

    def getAnnotator(self, name):
        return self.annotators[name]
    
    def asDict(self):
        return {
            'frames': self.framers[:],
            'annotators': self.annotators.keys(),
            'switchables': list(self.switchables)
        }
