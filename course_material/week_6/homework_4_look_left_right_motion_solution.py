#!/usr/bin/env python
import cv2
from example_2_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
from lib.robot import Robot
import time

import cv2
import numpy as np
import dlib
from imutils import face_utils
color_green = (0,255,0)

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize camera
    camera = Camera()
    # Start camera
    camera.start()
    # Initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    # Initalize robot
    robot = Robot()
    # Start robot
    robot.start()
    robot.move(0,0.5)


    # Loop
    while True:
        # Get image
        img = camera.getImage()

        # Get face detections
        dets = face_detector.detect(img)

        # Draw all face detections
        for det in dets:
            cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, 3)

        # We only use 1 face to estimate pose
        if(len(dets)>0):
            # Estimate pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, dets[0])
            # Draw pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)

            #TODO: find a yaw value from rotation_vector
            print rotation_vector
            yaw = rotation_vector[2]

            #TODO: remember current position
            print ("Pan angle is ",robot.getPosition()[0], "Tilt angle is", robot.getPosition()[1])
            current_pan = robot.getPosition()[0]
            current_tilt = robot.getPosition()[1]

            #TODO: insert the condition for looking at right
            if yaw > 0.3:
                print ('You are looking at right.')            
                #TODO: add motion for looking at right 
                robot.move(0.5,0.5)

            #TODO: insert the condition for looking at left
            elif yaw < -0.3:
                print ('You are looking at left.')            
                #TODO: add motion for looking at left 
                robot.move(-0.5,0.5)
           
            time.sleep(3)

            #TODO: Looking at the position that is stored.
            robot.move(current_pan,current_tilt)
            time.sleep(5)

        # Show image
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
