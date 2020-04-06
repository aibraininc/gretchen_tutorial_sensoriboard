#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

#initalize camera
camera = Camera()
#initalize robot
robot = Robot()


def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #start camera
    camera.start()
    #start robot
    robot.start()
    #initalize ball detector

    #TODO: cutomize your ball detector
    ball_detector = BallDetector()

    #count
    cnt = 0

    #loop
    while True:
        #get image from camera
        img = camera.getImage()
        (img, center) = ball_detector.detect(img)
        cv2.imshow("Frame", img[...,::-1])

        key = cv2.waitKey(1)
        if key > 0:
            break

        #TODO: track ball with camera and robot lib
        

if __name__ == '__main__':
    main()
