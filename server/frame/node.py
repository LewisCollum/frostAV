def addObserverToSubjects(observer, *subjects):
    for subject in subjects: subject.addObservers(observer)

class Node:
    def __init__(self, subject, strategy):
        self.subject = subject
        self.strategy = strategy        
        self.observers = []
        self.output = None

        if subject is not None:
            try:
                iter(self.subject)
                addObserverToSubjects(self, *self.subject)
            except:
                addObserverToSubjects(self, self.subject)
                
    def addObservers(self, *observers):
        self.observers += observers
        
    def __call__(self, package):
        self.output = self.strategy(package)
        for observer in self.observers:
            observer(self.output)

    def pull(self):
        return self.output
