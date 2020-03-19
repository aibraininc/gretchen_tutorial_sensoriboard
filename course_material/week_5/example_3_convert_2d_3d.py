#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
camera = Camera()
from lib.ros_environment import ROSEnvironment

def onMouse(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(u,v)
        (x,y,z) = camera.convert2d_3d(u,v)
        print (x,y,z,'on camera axis')
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print (x,y,z,'on robot axis')

def main():
    ROSEnvironment()
    camera.start()
    
    while True:
        img = camera.getImage()
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()

