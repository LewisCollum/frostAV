from .switchable import Switchables

class Model:
    def __init__(self):
        self.model = {}
        self.annotators = []
        self.framers = []
        self.switchables = Switchables()
        self.headName = None

    def setHead(self, headName):
        self.headName = headName

    @property
    def head(self): return self.get(self.headName)
        
    def add(self, name, node):
        self.model[name] = node
        
    def addAnnotator(self, name, node):
        self.add(name, node)
        self.annotators.append(name)

    def addFramer(self, name, node):
        self.add(name, node)
        self.framers.append(name)

    def addSwitchable(self, name, node):
        self.add(name, node)
        self.switchables.add(name, node)
        
    def get(self, name):
        return self.model[name]
        
    def asDict(self):
        return {
            'frames': self.framers[:],
            'annotations': self.annotators[:],
            'switchables': list(self.switchables)
        }
