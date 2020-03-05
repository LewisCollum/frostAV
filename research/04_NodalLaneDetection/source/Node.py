class Node:
    def __init__(self, strategy, distributor):
        self.strategy = strategy
        self.distributor = distributor

    def __call__(self, package):
        self.distributor(self.strategy(package))
