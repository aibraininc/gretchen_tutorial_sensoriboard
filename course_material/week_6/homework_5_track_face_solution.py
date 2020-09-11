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
    detector = dlib.get_frontal_face_detector()

    # The variable for counting loop
    cnt = 0

    # Loop
    while True:
        # Get image
        img = camera.getImage()

        # Get face detections
        dets = detector(img, 1)
        for det in dets:
            cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, 3)

        if (len(dets)>0):
            tracked_face = dets[0]
            tracked_face_x = (tracked_face.left()+tracked_face.right())/2
            tracked_face_y = (tracked_face.top()+tracked_face.bottom())/2
            (x,y,z) = camera.convert2d_3d(tracked_face_x, tracked_face_y)
            (x,y,z) = camera.convert3d_3d(x,y,z)
            robot.lookatpoint(x,y,z)
        # Show image
        cv2.imshow("Frame", img[...,::-1])

        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
