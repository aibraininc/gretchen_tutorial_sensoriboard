#!/usr/bin/env python
import cv2
import sys
from homework_1_ball_detector import BallDetector
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

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
        # Detect ball
        (img, center) = ball_detector.detect(img, 640)
        # Show ball
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break
        # Track ball
        if(center!= None):
            # Convert 2d coordinates to 3d coordinates on camera axis
            (x,y,z) = camera.convert2d_3d(center[0], center[1])
            print (x,y,z,'on camera axis')
            # Convert 3d coordinates on camera axis to 3d coordinates on robot axis
            (x,y,z) = camera.convert3d_3d(x,y,z)
            print (x,y,z,'on robot axis')
            # Move robot to look at 3d point
            robot.lookatpoint(x,y,z, 4, waitResult = False)

if __name__ == '__main__':
    main()
