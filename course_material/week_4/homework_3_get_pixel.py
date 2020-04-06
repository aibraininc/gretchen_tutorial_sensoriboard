#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera

#Initalize global camera
camera = Camera()
#Initalize global point
point = (0,0)

#Method triggered on click
def onMouse(event, u, v, flags, param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        img = camera.getImage()
   
	# it is pixel you clicked
        pixel = (u,v)
        print('Pixel', pixel)
        print('BGR', img[v,u])


def main():
    global point
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Starting camera
    camera.start()
    #loop
    while True:
        #gets image from camera
        img = camera.getImage()
        #draw circle on the point coordinate
        cv2.circle(img, point, 10, (0, 0, 255), -1)
        #show image
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()
