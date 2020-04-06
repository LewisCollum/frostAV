class Switchable:
    def __init__(self, node):
        self.node = node
        self.isOn = False

    @property
    def isOff(self): return not self.isOn
    
    @property
    def output(self): return self.node.output
        
    def addObservers(self, observers):
       self.node.addObservers(observers)
        
    def __call__(self, package):
        return self.node(package) if self.isOn else package

    def turnOn(self): self.isOn = True
    def turnOff(self): self.isOn = False

    
class Switchables:
    def __init__(self):
        self.switchables = {}

    def add(self, name, switchable):
        self.switchables[name] = switchable
                        
    def matchNames(self, others):
        self.turnOffNonMatching(others)
        self.turnOnMatching(others)

    def turnOffNonMatching(self, others):
        for name in self.switchables.keys():
            if name not in others:
                self.switchables[name].turnOff()
        
    def turnOnMatching(self, others):
        for other in others:
            node = self.switchables[other]
            if node.isOff:
                node.turnOn()
    
    def __iter__(self):
        for key in self.switchables.keys():
            yield key
