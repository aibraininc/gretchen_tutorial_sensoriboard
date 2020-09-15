#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

# Initalize global camera
camera = Camera()

def main():
    global point
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Start camera
    camera.start()
    # loop
    while True:
        # Get image from camera
        img = camera.getImage()

        #TODO: set set the boundaries for the box
        i_min = 280
        i_max = 360
        j_min = 200
        j_max = 280

        # Draw rectangle on the image
        for i in range(i_min, i_max):
            for j in range(j_min,j_max):
                #TODO: change the pixel to another color                
                img[j][i] = [255, 0, 0]
        # Show image
        cv2.imshow("Frame", img[...,::-1])

        # Close if key is pressed
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
