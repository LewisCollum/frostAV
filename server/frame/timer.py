import time 

class Timer:
    initialTime = None
    def __init__(self, node):
        self.node = node

    @property
    def name(self):
        return self.node.name

    def addObservers(self, observers):
        self.node.addObservers(observers)
        
    def __call__(self, unused):
        if self.initialTime:
            self.node(time.time() - self.initialTime)
            self.initialTime = None
        else:
            self.initialTime = time.time()

    def pull(self):
        return self.node.pull()
