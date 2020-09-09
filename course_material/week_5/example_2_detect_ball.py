#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize camera
    camera = Camera()
    # Start camera
    camera.start()
    # Initalize ball detector
    ball_detector = BallDetector()

    #loop
    while True:
        # Get image
        img = camera.getImage()
        # Gets image with ball detected,
        (img, center) = ball_detector.detect(img)
        # Show image
        cv2.imshow("Frame", img[...,::-1])
        # Print the center 
        print(center)
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
