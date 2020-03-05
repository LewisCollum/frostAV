class SingleDistributor:
    def __init__(self, receiver = None):
        self.receiver = receiver
        
    def __call__(self, package):
        self.receiver(package)

    def connect(self, receiver):
        self.receiver = receiver
        
    def disconnect(self):
        self.receiver = None
        
    
class MultiDistributor:
    def __init__(self, receivers = []):
        self.receivers = receivers

    def __call__(self, package):
        for receiver in self.receivers:
            receiver(package)
        
    def connect(self, receiver):
        self.receivers.append(receiver)

    def disconnect(self):
        self.receivers.clear()

        
class NamingDistributor:
    def __init__(self):
        self.receivers = {}

    def __call__(self, package):
        for receiver in self.receivers[pk.PackageConfig.nameFromDict(package)]:
            receiver.onReceivedPackage(package)
        
    def connect(self, name: str, receiver):
        self.receivers.setdefault(name, []).append(receiver)
        
    def disconnect(self):
        self.receivers.clear()
