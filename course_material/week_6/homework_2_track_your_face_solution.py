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
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #start camera
    focal_length = 640

    camera.start()

    robot = Robot()
    #start robot
    robot.start()
    #initalize face detector
    face_detector = FaceDetector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    #counter
    cnt =  1
    #loop
    while True:
        #get image
        img = camera.getImage()

        #gets face detections
        dets = face_detector.detect(img)

        #draw all face detections
        for det in dets:
            cv2.rectangle(img,(det.left(), det.top()), (det.right(), det.bottom()), color_green, 3)

        if(len(dets)>0):

            face_tracking = None
            distanceFromCenter_min = 1000
            # find a face near image center
            for face in dets:
                face_x = (face.left()+face.right())/2

                #TODO: write a distance between face and center, center of width is 320.
                distanceFromCenter = abs(face_x - 320)
                
                if distanceFromCenter <distanceFromCenter_min:
                    distanceFromCenter_min = distanceFromCenter
                    face_tracking = face

            #estimate pose
            (success, rotation_vector, translation_vector, image_points) = face_detector.estimate_pose(img, face_tracking)
            #draw pose
            img = face_detector.draw_pose(img, rotation_vector, translation_vector, image_points)

            #TODO: converts 2d coordinates to 3d coordinates on camera axis
            (x,y,z) = camera.convert2d_3d((face_tracking.left()+face_tracking.right())/2, (face_tracking.top()+face_tracking.bottom())/2)
            print (x,y,z,'on camera axis')

            #TODO: converts 3d coordinates on camera axis to 3d coordinates on robot axis
            (x,y,z) = camera.convert3d_3d(x,y,z)
            print (x,y,z,'on robot axis')
            #move robot
            robot.lookatpoint(x,y,z, 4, waitResult = False)

        #show image
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
