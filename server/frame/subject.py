import threading 
import time
import warnings

class Subject:
    def __init__(self, strategy, delay = 0):
        self.strategy = strategy
        self.delay = delay
        self.output = None
        self.observers = {}

    def addObservers(self, *observers):
        for observer in observers:
            self.observers[observer] = threading.Thread(target=self.observerLoop, args=(observer,))

    def start(self):
        self.isRunning = True
        self.thread = threading.Thread(target=self.loop)        
        self.thread.start()
        for observer in self.observers.keys():
            self.observers[observer] = threading.Thread(target=self.observerLoop, args=(observer,))
            self.observers[observer].start()

    def stop(self):
        self.isRunning = False
        for observerThread in self.observers.values():
            observerThread.join()
        self.thread.join()

    def removeObserver(self, observer):
        if self.isRunning:
            warnings.warn("Cannot remove observer while running", RuntimeWarning)
        else:
            del self.observers[observer]

    def loop(self):
        while self.isRunning:
            self.output = self.strategy()
            time.sleep(self.delay)

    def observerLoop(self, observer):
        while self.isRunning:
            if self.output is not None:
                observer(self.output)
            time.sleep(self.delay)

            
if __name__ == '__main__':
    subject = Subject(lambda: "test", delay = 0.05)

    def a(output): print(output)
    def b(output): print(output + " me")

    subject.addObservers(a, b)
    subject.start()
    time.sleep(0.1)
    # Does not remove observer
    print("trying to remove observer a")
    subject.removeObserver(a)
    time.sleep(0.1)    
    subject.stop()
    # Works without warning
    print("trying to remove observer a")    
    subject.removeObserver(a)
    subject.start()
    time.sleep(0.3)
    subject.stop()

    
