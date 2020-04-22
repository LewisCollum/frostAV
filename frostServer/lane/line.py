import numpy
from collections import namedtuple

LaneRegion = namedtuple('LaneLines', ['left', 'right'])
Line = namedtuple('Line', ['x1','y1','x2','y2'])
