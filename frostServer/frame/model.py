class Model:
    def __init__(self, subject):
        self.subject = subject
        self.model = {}
        self.annotators = []
        self.framers = []
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

    def get(self, name):
        return self.model[name]
        
    def connect(self):
        self.subject.addObserver(self, self.get(self.headName))

    def disconnect(self):
        self.subject.removeObserver(self)
