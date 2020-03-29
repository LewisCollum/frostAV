import cv2
import sys
import threading 

source = sys.argv[1] if len(sys.argv) > 1 else 0
observers = []
currentFrame = None

def getCurrentFrame():
    return currentFrame

def addObservers(others):
    global observers
    observers += others

def grabCaptureFrame():
    capture = cv2.VideoCapture(source)
    _, frame = capture.read()
    capture.release()
    return frame

def startCapture():
    capture = cv2.VideoCapture(source)
    while True: #cv2.waitKey(33) != ord('q'):
        print("anotha one")
        hasFrame, frame = capture.read()
        if hasFrame:
            global currentFrame
            currentFrame = frame
            for observer in observers: observer(currentFrame)

captureThread = None
def startThreadedCapture():
    global captureThread
    if captureThread == None:
        captureThread = threading.Thread(target=startCapture)
        captureThread.start()

def stop():
    capture.release()
    cv2.destroyAllWindows()
