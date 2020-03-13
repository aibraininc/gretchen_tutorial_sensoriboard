#!/usr/bin/env python
import cv2
import rospy
import sys
sys.path.append('../../')
from lib.camera import Camera


def onMouse(camera, u, v):
    print(u, v)
    (x,y,z) = camera.convert2d_3d(u,v)
    print ('camera',x,y,z)
    (x,y,z) = camera.convert3d_3d(x,y,z)
    print ('robot',x,y,z)
    
def main():
    camera = Camera(click=onMouse)
    camera.start()

    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        frame = camera.image
        camera.showImage(frame)
        rate.sleep()

if __name__ == '__main__':
    main()
