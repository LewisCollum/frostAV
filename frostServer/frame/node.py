def addObserverToSubjects(observer, subjects):
    for subject in subjects: subject.addObservers(observer)

class Node:
    def __init__(self, name, subjects, strategy):
        self.strategy = strategy
        self.observers = []
        self.subjects = subjects
        self.output = None
        self.name = name
        addObserverToSubjects(self, self.subjects)
        
    def addObservers(self, *observers):
        self.observers += observers
        
    def __call__(self, package):
        self.output = self.strategy(package)
        for observer in self.observers:
            observer(self.output)

    def pull(self):
        return self.output
