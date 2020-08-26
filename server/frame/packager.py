from collections import namedtuple

from .node import Node

Package = namedtuple('Package', ['name', 'content'])

class Packager:
    def __init__(self, name, node):
        self.name = name
        self.node = node
        self.packagingNode = Node(
            subject = self.node,
            strategy = lambda content: Package(self.name, content))

    def pull(self):
        return self.node.pull()
    
    def addObservers(self, observers):
        self.packagingNode.addObservers(observers)
        
    def __call__(self, content):
        self.packagingNode(content)
