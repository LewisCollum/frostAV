from .node import Node

class Joiner(Node):
    def __init__(self, name, subjects, strategy):
        super().__init__(name, subjects, strategy)
        self.packages = self.makeEmptyPackages()
        
    def __call__(self, package):
        self.packages[package.name] = package.content

        if self.hasPackageFromEachSubject():
            super().__call__(self.packages)
            self.packages = self.makeEmptyPackages()
                        
    def hasPackageFromEachSubject(self):
        return None not in self.packages.values()
        
    def makeEmptyPackages(self):
        return dict.fromkeys([subject.name for subject in self.subjects])
