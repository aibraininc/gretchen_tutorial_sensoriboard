#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

#Initalize camera
camera = Camera()

#method that is called when mouse is clicked
def onMouse(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(u,v)
        #coverts the pixel to 3d coordinates on camera axis
        (x,y,z) = camera.convert2d_3d(u,v)
        print (x,y,z,'on camera axis')
        #converts 3d coordinates on camera axis to 3d coordinates on robot axis
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print (x,y,z,'on robot axis')

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Starts camera
    camera.start()
    #loop
    while True:
        #gets image from camera
        img = camera.getImage()
        #shows image 
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
