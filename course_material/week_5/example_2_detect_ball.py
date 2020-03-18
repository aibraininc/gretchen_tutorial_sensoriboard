#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera

def main():
    rospy.init_node('camera_show', anonymous=True)
    camera = Camera()
    camera.start()
    ball_detector = BallDetector()
    
    while True:
        img = camera.getImage()
        (img, centor) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        print(centor)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()

