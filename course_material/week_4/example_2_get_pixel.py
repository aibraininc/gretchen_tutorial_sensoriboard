#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.camera_v2 import Camera
camera = Camera()
point = (0,0)

def onMouse(event, u, v, flags, param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        img = camera.getImage()
        point = (u,v)
        print('Point', u,v)
        print('BGR', img[v,u])

def main():
    global point
    ROSEnvironment()
    camera.start()
    
    while True:
        img = camera.getImage()
        cv2.circle(img, point, 10, (0, 0, 255), -1)
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        key = cv2.waitKey(1)
        if key > 0:
            break

if __name__ == '__main__':
    main()

