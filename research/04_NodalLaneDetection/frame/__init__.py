from . import subject
from .displayer import Displayer, LineDisplayer
from .line import addLines

import cv2
def toImage(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()
