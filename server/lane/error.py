def handleNoLane(laneAngles):
    pass

def handleLane(laneAngles):
    return laneAngles.left - laneAngles.right

class HandleLeftOnly:
    def __init__(self, perspectiveAngle):
        self.perspectiveAngle = perspectiveAngle

    def __call__(self, laneAngles):
        return 2*(laneAngles.left - self.perspectiveAngle)

    
class HandleRightOnly:
    def __init__(self, perspectiveAngle):
        self.perspectiveAngle = perspectiveAngle

    def __call__(self, laneAngles):
        return 2*(self.perspectiveAngle - laneAngles.right)
    
    
class Error:
    def __init__(self, stateNodeName, anglesNodeName, perspectiveAngle):
        self.stateNodeName = stateNodeName
        self.anglesNodeName = anglesNodeName
        self.error = 0
        self.stateModel = {
            'NoLane': lambda laneAngles: self.error,
            'Lane': handleLane,
            'LeftOnly': HandleLeftOnly(perspectiveAngle),
            'RightOnly': HandleRightOnly(perspectiveAngle)}
        
    def __call__(self, packages):
        state = packages[self.stateNodeName]
        angles = packages[self.anglesNodeName]

        self.error = self.stateModel[state](angles)
        return self.error


from enum import Enum, auto
from collections import namedtuple
CrossTurn = namedtuple('CrossTurn', ['turnAngles', 'crossTrackAngles'])

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class CrossTurnError:
    def __init__(self, stateNodeName, turnAnglesNodeName, crossTrackAngleNodeName, perspectiveAngle):
        self.stateNodeName = stateNodeName
        self.turnAnglesNodeName = turnAnglesNodeName
        self.crossTrackAngleNodeName = crossTrackAngleNodeName
        self.perspectiveAngle = perspectiveAngle
        self.error = 0
        self.headed = Direction.LEFT        
        self.stateModel = {
            'NoLane': lambda crossTurn: self.error,
            'Lane': self.handleLane,
            'LeftOnly': self.leftOnly,
            'RightOnly': self.rightOnly}
        
    def __call__(self, packages):
        state = packages[self.stateNodeName]
        turnAngles = packages[self.turnAnglesNodeName]
        crossTrackAngles = packages[self.crossTrackAngleNodeName]

        crossTurn = CrossTurn(turnAngles = turnAngles, crossTrackAngles = crossTrackAngles)
        self.error = self.stateModel[state](crossTurn)
        print(f"Headed: {self.headed}")
        return self.error

    def handleLane(self, crossTurn):
        left, right = crossTurn.crossTrackAngles
        return left - right
    
    def leftOnly(self, crossTurn):
        lineAngle = crossTurn.turnAngles.left
        if lineAngle <= self.perspectiveAngle:
            self.headed = Direction.LEFT
        else:
            self.headed = Direction.RIGHT        
        return self.lineAngleError(lineAngle)
    
    def rightOnly(self, crossTurn):
        lineAngle = crossTurn.turnAngles.right
        if lineAngle <= self.perspectiveAngle:
            self.headed = Direction.RIGHT
        else:
            self.headed = Direction.LEFT
        return self.lineAngleError(lineAngle)

    def lineAngleError(self, lineAngle):
        error = self.errorFromAngle(lineAngle)
        return error
        #return error if self.headed == Direction.RIGHT else -error
            
    def errorFromAngle(self, lineAngle):
        return 2*(lineAngle - self.perspectiveAngle)
        
    def directionFromThresholdAngle(self, lineAngle):
        if lineAngle <= self.perspectiveAngle:
            return Direction.RIGHT
        else:
            return Direction.LEFT
    
