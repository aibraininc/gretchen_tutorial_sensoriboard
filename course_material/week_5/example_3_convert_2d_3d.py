#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera

def onMouse(camera, u, v):
    print(u, v)
    (x,y,z) = camera.convert2d_3d(u,v)
    print (x,y,z,'on camera axis')
    (x,y,z) = camera.convert3d_3d(x,y,z)
    print (x,y,z,'on robot axis')

def main():
    rospy.init_node('camera_show', anonymous=True)
    camera1 = Camera(click=onMouse)
    camera1.start()
    
    while(True):
        img = camera1.getImage()
        camera1.showImage(img)

if __name__ == '__main__':
    main()

