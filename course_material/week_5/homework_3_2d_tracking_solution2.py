#!/usr/bin/env python
import cv2
import sys
from homework_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

# Initalize camera
camera = Camera()
# Initalize robot
robot = Robot()

def calculateDistance(center):
    x_distance = center[0] -320
    y_distance = center[1] -240
    return [x_distance, y_distance]

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Start robot
    robot.start()
    # Initalize ball detector
    ball_detector = BallDetector()

    #boundaries
    ball_on_right = -100
    ball_on_left = 100
    ball_on_bottom = -100
    ball_on_top = 100

    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
        # Detect ball
        (img, center) = ball_detector.detect(img)
        # Show ball
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break
        # Track ball
        if(center!= None):
            print center[0], center[1]
            #TODO: calculate distance between detected ball and the image center.
            distance = calculateDistance(center)

            pan = robot.getPosition()[0]
            tilt = robot.getPosition()[1]
            pan_delta = 0.15
            tilt_delta = 0.15

            #TODO: move motor on x-axis using move function
            if distance[0]> ball_on_left:
                pan = pan - pan_delta
            elif distance[0] < ball_on_right:
                pan = pan + pan_delta
            #TODO: move motor on y-axis using move function
            if distance[1]> ball_on_top:
                tilt = tilt - tilt_delta
            elif distance[1] < ball_on_bottom:
                tilt = tilt + tilt_delta

            robot.move(pan,tilt)


if __name__ == '__main__':
    main()
