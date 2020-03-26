#!/usr/bin/env python
import cv2
from example_1_face_detector import FaceDetector
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize camera
    camera = Camera()
    #start camera
    camera.start()
    #initalize face detector
    face_detector = FaceDetector()
    #loop
    while True:
        #get image
        img = camera.getImage()
        #gets image with face detection, center value
        [img,center] = face_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        
        key = cv2.waitKey(1)
        if key > 0:
            break


if __name__ == '__main__':
    main()
