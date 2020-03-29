import cv2
import sys
import threading 

source = 0
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
        hasFrame, frame = capture.read()
        print(f"SUBJECT READ: {hasFrame}")
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
