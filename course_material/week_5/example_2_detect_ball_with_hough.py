#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment
import numpy as np

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #Start camera
    camera.start()
    #Initalize ball detector
    ball_detector = BallDetector()

    #loop
    while True:
        #get image
        img = camera.getImage()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.erode(gray, None, iterations=2)
        gray = cv2.dilate(gray, None, iterations=2)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.4, 100)
        # circles = cv2.HoughCircles(gray,  
        #                 cv2.HOUGH_GRADIENT, 1, 100, param1 = 50, 
        #             param2 = 30, minRadius = 1, maxRadius = 40) 


        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        # show the output image
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
