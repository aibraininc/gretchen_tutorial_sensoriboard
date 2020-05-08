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

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #start camera
    focal_length = 640

    camera.start()
    #initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    #loop
    while True:
        #get image
        img = camera.getImage()

        #gets face detections
        dets = face_detector.detect(img)

        #draw all face detections
        for det in dets:
            cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, 3)

        #we only use 1 face to estimate pose
        if(len(dets)>0):
            #estimate pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, dets[0])
            #draw pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)
            print("rotation_vector")
            print rotation_vector
            print("translation_vector")
            print translation_vector
        #show image
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
