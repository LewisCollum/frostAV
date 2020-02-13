import os
from datetime import datetime

directory = "../runs"
current = os.path.join(directory, ".current")

class Run:
    def __init__(self, runName):
        run = os.path.join(directory, runName)
        self.model = os.path.join(run, "model.h5")
        self.log = os.path.join(run, "log.csv")
        self.accuracy = os.path.join(run, "accuracy.png")
        self.modelDiagram = os.path.join(run, "model.png")

def make():
    runName = f"{datetime.now():%m-%d_%H%M}"
    newRun = os.path.join(directory, runName)
    os.mkdir(newRun)
    with open(current, 'w') as f:
        f.write(runName)
    
def loadFromName(runName):
    return Run(runName)

def loadCurrent():
    with open(current) as f:
        return loadFromName(f.readline())

def has(path):
    return os.path.isfile(path)
