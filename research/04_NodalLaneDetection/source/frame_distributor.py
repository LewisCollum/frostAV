import cv2
import sys

import distributor

def startAtHead(head):
    frameDistributor = distributor.SingleDistributor(head)
    capture = cv2.VideoCapture(sys.argv[1])
    while cv2.waitKey(33) != ord('q'):
        global frame
        hasFrame, frame = capture.read()
        if not hasFrame: break
        frameDistributor(frame)
        
    cv2.waitKey(0)
    capture.release()
    cv2.destroyAllWindows()
