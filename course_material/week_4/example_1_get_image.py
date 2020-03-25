#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    while True:
        img = camera.getImage()
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break


if __name__ == '__main__':
    main()
