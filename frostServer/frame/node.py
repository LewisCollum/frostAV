class Node:
    def __init__(self, subjects, strategy):
        self.strategy = strategy
        self.observers = []
        for subject in subjects: subject.addObservers([self])
        self.output = None
                
    def addObservers(self, observers):
        self.observers += observers
        
    def __call__(self, package):
        self.output = self.strategy(package)
        for observer in self.observers:
            observer(self.output)
