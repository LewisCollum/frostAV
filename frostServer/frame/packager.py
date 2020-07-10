from collections import namedtuple

from .node import Node

Package = namedtuple('Package', ['name', 'content'])

class Packager:
    def __init__(self, node):
        self.node = node
        self.packagingNode = Node(
            name = None,
            subjects = [self.node],
            strategy = lambda content: Package(self.node.name, content))

    @property
    def name(self):
        return self.node.name

    def pull(self):
        return self.node.pull()
    
    def addObservers(self, observers):
        self.packagingNode.addObservers(observers)
        
    def __call__(self, content):
        self.packagingNode(content)
