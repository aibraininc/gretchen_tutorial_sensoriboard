#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

# Initalize camera
camera = Camera()

# Method that is called when pixel is clicked
def onMouse(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(u,v)
        # Convert the pixel to 3d coordinates on camera axis
        (x,y,z) = camera.convert2d_3d(u,v)
        print (x,y,z,'on camera axis')
        # Convert 3d coordinates on camera axis to 3d coordinates on robot axis
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print (x,y,z,'on robot axis')

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # Loop
    while True:
        # Get image from camera
        img = camera.getImage()
        # Show image 
        cv2.imshow("Frame", img[...,::-1])
        # When you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
