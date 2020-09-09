#!/usr/bin/env python
import cv2
from example_2_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
from lib.robot import Robot

from time import time, sleep
import cv2
import numpy as np
import dlib
from imutils import face_utils
color_green = (0,255,0)

# get current time (s)
def current_time():
    return time()

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


    # the time when motion runs
    motion_start_time = None

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

            #TODO: insert the condition for looking at right
            if (yaw > 0.3 and motion_start_time == None):
                print ('You are looking at right.')
                current_pan =
                current_tilt =

                #TODO: add motion for looking at right
                robot.move(,)

                motion_start_time = current_time()

            #TODO: insert the condition for looking at left
            elif (yaw < -0.3 and motion_start_time == None):
                    print ('You are looking at left.')
                    current_pan =
                    current_tilt =

                    #TODO: add motion for looking at left
                    robot.move(,)

                    motion_start_time = current_time()
            if(motion_start_time !=None):
                print current_time()- motion_start_time

        # After the motion runs, check if 3 seconds have passed.
        if(motion_start_time != None and current_time()-motion_start_time > 3 ):
            #TODO: Looking at the position that is stored.
            robot.move(, )
            motion_start_time = None

        sleep(0.05)
        # Show image
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
