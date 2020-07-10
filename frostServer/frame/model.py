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
        
    def add(self, node):
        self.model[node.name] = node
        
    def addFramer(self, node):
        self.add(node)
        self.framers.append(node.name)

    def addSwitchable(self, node):
        self.add(node)
        self.switchables.add(node.name, node)
        
    def addAnnotator(self, annotator):
        self.annotators[annotator.name] = annotator
        
    def get(self, name):
        return self.model[name]

    def __getitem__(self, name):
        return self.model[name]
    
    def getAnnotator(self, name):
        return self.annotators[name]

    @property
    def toggleNames(self):
        return {
            'Annotation': self.annotators.keys(),
            'Switchable': list(self.switchables)
        }

    @property
    def radioNames(self):
        return {
            'Frame': self.framers[:]
        }
