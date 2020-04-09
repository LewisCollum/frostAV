import cv2

from . import line


def toImage(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()

class Imager:
    def __init__(self, defaultSubject):
        self.subject = defaultSubject
        self.annotatorNodes = []
        
    def __iter__(self):
        while True:
            outputFrame = self.subject.output
            if outputFrame is not None:
                outputFrame = self.addAnnotators(outputFrame)
                image = toImage(outputFrame)
                yield image

    def addAnnotators(self, frame):
        isAnnotatable = len(self.annotatorNodes) > 0 and len(frame.shape) == 3 and frame.shape[2] == 3
        if isAnnotatable:
            for annotatorNode in self.annotatorNodes:
                frame = cv2.addWeighted(frame, 0.8, annotatorNode(), 1, 1, dtype = cv2.CV_32F)
        return frame

class ImageResponder:
    def __init__(self, imager):
        self.imager = imager

    def __iter__(self):
        for image in self.imager:
            yield self.asImageResponse(image)

    def asImageResponse(self, image):
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n'       
