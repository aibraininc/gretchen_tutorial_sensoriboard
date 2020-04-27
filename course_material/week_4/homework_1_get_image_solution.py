#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initialize camera
    camera = Camera()
    #Start camera
    camera.start()

    #loop
    while True:
        #TODO: Get image from camera, getImage returns an image
        img = camera.getImage()
        #Use opencv to show image on window named "Frame"
        cv2.imshow("Frame", img[...,::-1])
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
