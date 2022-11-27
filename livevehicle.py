from imutils.video import VideoStream
from imutils.video import FPS
import numpy.core.multiarray
import numpy as np
import argparse
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
from imutils.video import FileVideoStream


def video():
    print("[INFO] starting video stream...")
    vs = FileVideoStream("cars.mp4").start()
    time.sleep(1.0)
    fps = FPS().start()
    writer = None
    (W, H) = (None, None)
    while True:
        # grab the frame from the thr
        # read the next frame from the file
        frame = vs.read()
        frame=imutils.resize(frame,width=912)
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            writer = cv2.VideoWriter('live_video.mp4', fourcc, 5,
                (frame.shape[1], frame.shape[0]), True)
            
        # show the output frame
        writer.write(frame)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        fps.update()
    fps.stop()
    # do a bit of cleanup
    writer.release()
    cv2.destroyAllWindows()
    vs.stop()
if __name__=='__video__':
    video()