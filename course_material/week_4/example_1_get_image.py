#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera

def main():
    rospy.init_node('camera_show', anonymous=True)
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
