import cv2
import numpy as np

def makeCpuDarknet(configurationPath, weightsPath):
    net = cv2.dnn.readNetFromDarknet(configurationPath, weightsPath)
    #net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net

def readClasses(classesPath):
    with open(classesPath, 'rt') as f:
        return f.read().rstrip('\n').split('\n')
           
class Net:
    def __init__(self, net):
        self.net = net
        self.outputNames = self.outputNamesFromNet()

    def outputNamesFromNet(self):
        layerNames = self.net.getLayerNames()
        return [layerNames[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
    def __call__(self, blob):
        print("NET CALL")
        self.net.setInput(blob)
        print("INPUTTED")
        return self.net.forward(self.outputNames)

    
# Remove the bounding boxes with low confidence using non-maxima suppression
class DetectionBoxes:
    def __init__(self, frameShape, confidenceThreshold, nonMaxSuppressionThreshold):
        self.frameHeight = frameShape[0]
        self.frameWidth = frameShape[1]
        self.confidenceThreshold = confidenceThreshold
        self.nonMaxSuppressionThreshold = nonMaxSuppressionThreshold
        
    def __call__(self, outs):
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        print("START NMS")        
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confidenceThreshold:
                    center_x = int(detection[0] * self.frameWidth)
                    center_y = int(detection[1] * self.frameHeight)
                    width = int(detection[2] * self.frameWidth)
                    height = int(detection[3] * self.frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidenceThreshold, self.nonMaxSuppressionThreshold)

        detectionBoxes = []
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            detectionBoxes.append({
                'id': classIds[i],
                'confidence': confidences[i],
                'left': left,
                'right': left + width,
                'top': top,
                'bottom': top + height})

        print("DONE NMS")
        return detectionBoxes


class DrawDetectionBoxes:
    def __init__(self, classes):
        self.classes = classes

    def __call__(self, frame, detectionBoxes):
        if detectionBoxes is not None:
            for box in detectionBoxes:
                # Draw a bounding box.
                cv2.rectangle(frame, (box['left'], box['top']), (box['right'], box['bottom']), (255, 178, 50), 3)
                
                tag = self.classes[box['id']]
                label = f"{tag}: {box['confidence']:.2f}"        
                #Display the label at the top of the bounding box
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                
                top = max(box['top'], labelSize[1])
                cv2.rectangle(frame, (box['left'], top - round(1.5*labelSize[1])), (box['left'] + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (box['left'], top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)
        return frame
        
