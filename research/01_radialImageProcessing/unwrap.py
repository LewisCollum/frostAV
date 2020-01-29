import cv2
from unwrapper import SphereUnwrapper
import sys

def unwrap(filename):
  cv2.namedWindow("preview")
  capture = cv2.VideoCapture(filename)
  _, frame = capture.read()
  unwrapper = SphereUnwrapper.makeFromSize(frame.shape[0])

  unwrappedFrame = unwrapper.unwrap(frame)
  cv2.imshow("", unwrappedFrame)

  while capture.isOpened():
    _, frame = capture.read()
    if frame is not None:
      unwrappedFrame = unwrapper.unwrap(frame)
      cv2.imshow("", unwrappedFrame)

    if cv2.waitKey(1) == ord('q'):
      break

  capture.release()

unwrap(sys.argv[1])
cv2.destroyAllWindows()
cv2.waitKey(0)
