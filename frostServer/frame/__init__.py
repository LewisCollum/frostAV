from .displayer import Displayer, LineDisplayer
from .line import addLines
from .subject import Subject
from .model import Model
from .node import Node

import cv2
def toImage(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()
