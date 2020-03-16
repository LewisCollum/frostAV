class Node:
    def __init__(self, strategy, observers):
        self.strategy = strategy
        self.observers = observers

    def __call__(self, package):
        for observer in self.observers:
            observer(self.strategy(package))
