#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

# Initalize camera
camera = Camera()
# Initalize robot
robot = Robot()

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Start robot
    robot.start()
    # Initalize ball detector
    ball_detector = BallDetector()

    # The variable for counting loop
    cnt = 0

    # Loop
    while True:
        #TODO: get image from camera
        img = 
        #TODO: use ball_detector to detect ball
        (img, center) = 
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
