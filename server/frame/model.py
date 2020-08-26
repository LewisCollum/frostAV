from collections import defaultdict

from .switchable import Switchables

class Model:
    def __init__(self):
        self.model = defaultdict(dict)
        self.head = None
        self.previous = None

    def addNode(self, name, category, node):
        isHead = len(self.model.keys()) == 0

        self.model[category][name] = node

        if isHead: self.head = self(name, category)
        self.previous = self(name, category)

    def __call__(self, name, category):
        return self.model[category][name]
    
    def category(self, category):
        return self.model[category]
