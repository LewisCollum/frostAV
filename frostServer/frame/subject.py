import cv2
import sys
import threading 
import time 
        
class Subject:
    def __init__(self, source):
        self.capture = cv2.VideoCapture(source)
        self.frameShape = (
            int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            3)

        self.observers = {}
        self.output = None
    
    def addObserver(self, name, observer):
        self.observers[name] = observer

    def removeObserver(self, name):
        del self.observers[name]

    def startCapture(self):
        while True:
            hasFrame, frame = self.capture.read()
            if hasFrame:
                self.output = frame
            time.sleep(0.05)

    def startDistribution(self, observer):
        print(f"Distribution started for {observer}...")
        while True:
            if self.output is not None:
                observer(self.output)
                                
    def startThreadedCapture(self):
        threading.Thread(target=self.startCapture).start()
        for observer in self.observers.values():
            threading.Thread(target=self.startDistribution, args=(observer,)).start()            

    def stop():
        # self.captureThread.terminate()
        # self.captureThread = None
        self.capture.release()
