#!/usr/bin/env python
import cv2
from example_2_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
import cv2
import numpy as np
import dlib
from imutils import face_utils
color_green = (0,255,0)
from lib.robot import Robot

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize camera
    camera = Camera()
    # Start camera
    camera.start()

    # Initalize robot
    robot = Robot()
    # Start robot
    robot.start()
    # Initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    # The variable for counting loop
    cnt = 0

    # Loop
    while True:
        # Get image
        img = camera.getImage()

        # Get face detections
        dets = face_detector.detect(img)

        # Draw all face detections
        for det in dets:
            cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, 3)

        if(len(dets)>0):

            face_tracking = None
            distanceFromCenter_min = 1000
            # Find a face near image center
            for face in dets:
                face_x = (face.left()+face.right())/2

                #TODO: write a distance between face and center, center is 0.5*width of image.
                distanceFromCenter = 

                # Find a face that has the smallest distance
                if distanceFromCenter <distanceFromCenter_min:
                    distanceFromCenter_min = distanceFromCenter
                    face_tracking = face

            # Estimate pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, face_tracking)
            # Draw pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)

            #TODO: convert 2d coordinates to 3d coordinates on camera axis
            (x,y,z) = 
            print (x,y,z,'on camera axis')

            #TODO: convert 3d coordinates on camera axis to 3d coordinates on robot axis
            (x,y,z) = 
            print (x,y,z,'on robot axis')

            # Track ball lazely.
            cnt = cnt + 1
            if cnt % 50 == 0:
                #TODO: move robot for watching a face


        # Show image
        cv2.imshow("Frame", img[...,::-1])
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
