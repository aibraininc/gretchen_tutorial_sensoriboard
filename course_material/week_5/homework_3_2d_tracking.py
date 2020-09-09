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

def calculateDistance(ball_center):
    #Image size is 640x480
    image_center = [640/2, 480/2]
    x_distance = ball_center[0] - image_center[0]
    y_distance = ball_center[1] - image_center[1]
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
        (img, ball_center) = ball_detector.detect(img)
        # Show ball
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break
        # Track ball

        if(ball_center!= None):
            #TODO: calculate distance between detected ball and the image center.
            distance = calculateDistance(ball_center)
            print distance[0], distance[1]

            #TODO: move motor on x-axis using right and left function
            #Ball is on the left  
            if distance[0]> ball_on_left:
                #move robot

            #Ball is on the right  
            elif distance[0] < ball_on_right:
                #move robot
  
            #TODO: move motor on y-axis using up and down function
            #Ball is on the top           
            if distance[1]> ball_on_top:
                #move robot

            #Ball is on the bottom 
            elif distance[1] < ball_on_bottom:
                #move robot 


if __name__ == '__main__':
    main()
