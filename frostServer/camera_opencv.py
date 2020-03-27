import os
import cv2
import time
import threading

event = threading.Event()
currentFrame = None
readingThread = None
onFrame = lambda frame: frame

def startReading():
    global readingThread    
    global lastAccessTime
    lastAccessTime = time.time()
    if readingThread == None:
        readingThread = threading.Thread(target=readingHandler)
        readingThread.start()
        
def readingHandler():
    global currentFrame
    print('Starting camera thread.')
    for frame in frameGenerator():
        currentFrame = frame
        event.set()
        time.sleep(0)
        
        if time.time() - lastAccessTime > 10:
            frameGenerator().close()
            print('Stopping camera thread due to inactivity.')
            break

def frameGenerator():
    camera = cv2.VideoCapture(0)
    while True:
        isFrameRead, frame = camera.read()
        if isFrameRead:
            modifiedFrame = onFrame(frame)
            yield cv2.imencode('.jpg', modifiedFrame)[1].tobytes()

        
def getFrame():
    global lastAccessTime
    lastAccessTime = time.time()
    event.wait()
    event.clear()    
    return currentFrame
