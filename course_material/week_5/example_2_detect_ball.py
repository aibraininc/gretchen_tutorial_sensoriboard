#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ball_detector import BallDetector

def main():
    rospy.init_node('camera_show', anonymous=True)
    camera1 = Camera()
    camera1.start()
    ball_detector = BallDetector()
    
    while(True):
        img = camera1.getImage()
        (img, centor) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        cv2.waitKey(1)

if __name__ == '__main__':
    main()

