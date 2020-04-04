class Model:
    def __init__(self, subject):
        self.subject = subject
        self.model = {}
        self.annotators = []
        self.framers = []
        self.frameModifiers = []
        self.frameStrategyStorage = {}
        self.headName = None

    def setHead(self, headName):
        self.headName = headName

    def add(self, name, node):
        self.model[name] = node
        
    def addAnnotator(self, name, node):
        self.add(name, node)
        self.annotators.append(name)

    def addFramer(self, name, node):
        self.add(name, node)
        self.framers.append(name)

    def addFrameModifier(self, name, node):
        self.add(name, node)
        self.frameModifiers.append(name)
        self.frameStrategyStorage[name] = node.strategy

    def reconnectFrameModifier(self, name):
        if name in self.frameStrategyStorage:
            node = self.model.get(name)
            node.strategy = self.frameStrategyStorage[name]
            del self.frameStrategyStorage[name]
            self.framers.append(name)
            print('R', self.framers)
            
    def disconnectFrameModifier(self, name):
        if name not in self.frameStrategyStorage:
            node = self.model.get(name)
            self.frameStrategyStorage[name] = node.strategy
            node.strategy = lambda x: x
            self.framers.remove(name)
            print('D', self.framers)
        
    def get(self, name):
        return self.model[name]
        
    def connect(self):
        self.subject.addObserver(self, self.get(self.headName))

    def disconnect(self):
        self.subject.removeObserver(self)
