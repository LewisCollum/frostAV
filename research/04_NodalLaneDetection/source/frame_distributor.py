import cv2
import sys

source = sys.argv[1] if len(sys.argv) > 1 else 0
observers = []

def grabCaptureFrame():
    capture = cv2.VideoCapture(source)
    _, frame = capture.read()
    capture.release()
    return frame
    
def sendCapture():
    capture = cv2.VideoCapture(source)
    while cv2.waitKey(33) != ord('q'):
        global frame
        hasFrame, frame = capture.read()
        if not hasFrame: break
        for observer in observers: node(frame)
        
    cv2.waitKey(0)
    capture.release()
    cv2.destroyAllWindows()


def sendFrame(externalFrame):
    global frame
    frame = externalFrame
    for observer in observers: observer(frame)
