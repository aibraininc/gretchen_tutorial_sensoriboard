#!/usr/bin/env python
import cv2
import rospy
import sys
sys.path.append('../../')
from lib.camera import Camera
from lib.robot import Robot
from lib.ball_detector import BallDetector
robot = None
    


def main():
    global robot
    robot = Robot()
    camera = Camera()
    camera.start()
    ball_detector = BallDetector()


    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        frame = camera.image
        (image, centor) = ball_detector.detect(frame, 640)
        print(centor)
        camera.showImage(image)
        rate.sleep()

if __name__ == '__main__':
    main()
