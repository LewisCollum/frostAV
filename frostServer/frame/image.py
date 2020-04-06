import cv2

from . import line


def toImage(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()

class Imager:
    def __init__(self, defaultSubject):
        self.subject = defaultSubject
        self.annotationNodes = []
        
    def __iter__(self):
        while True:
            outputFrame = self.subject.output
            if outputFrame is not None:
                outputFrame = self.addAnnotations(outputFrame)
                image = toImage(outputFrame)
                yield image

    def addAnnotations(self, frame):
        isAnnotatable = len(self.annotationNodes) > 0 and len(frame.shape) == 3 and frame.shape[2] == 3
        if isAnnotatable:
            for annotationNode in self.annotationNodes:
                frame = line.addLines(frame, annotationNode.output)
        return frame

class ImageResponder:
    def __init__(self, imager):
        self.imager = imager

    def __iter__(self):
        for image in self.imager:
            yield self.asImageResponse(image)

    def asImageResponse(self, image):
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image + b'\r\n'       
