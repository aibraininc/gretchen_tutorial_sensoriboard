#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment

#Initalize camera
camera = Camera()
#Intalize point
point = (0,0)

#Method called when clicked
def onMouse(event, u, v, flags, param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        img = camera.getImage()
        #changes image to hsv color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        point = (u,v)
        print('Point', u,v)
        #prints color RGB
        print('RGB', img[v,u])
        #prints color HSV
        print('HSV', hsv[v,u])

def main():
    global point
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Start camera
    camera.start()
    #loop
    while True:
        #Gets image from camera
        img = camera.getImage()
        #Draws circle on point
        cv2.circle(img, point, 10, (0, 0, 255), 3)
        #Shows image
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        key = cv2.waitKey(1)
        if key > 0:
            break



if __name__ == '__main__':
    main()
