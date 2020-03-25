#!/usr/bin/env python
import cv2
from example_1_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    face_detector = FaceDetector()

    while True:
        img = camera.getImage()
        [img,centors] = face_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break


if __name__ == '__main__':
    main()
