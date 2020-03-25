#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    ball_detector = BallDetector()
    
    while True:
        img = camera.getImage()
        (img, centor) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        print(centor)
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()

