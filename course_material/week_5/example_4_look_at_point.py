#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
robot = None

def onMouse(camera1, u, v):
    print(u, v)
    (x,y,z) = camera1.convert2d_3d(u,v)
    print (x,y,z,'on camera axis')
    (x,y,z) = camera1.convert3d_3d(x,y,z)
    print (x,y,z,'on robot axis')

    global robot
    robot.lookatpoint(x,y,z, waitResult = False)
    print('look at point end')

def main():
    rospy.init_node('camera_show', anonymous=True)
    global robot
    robot = Robot()

    camera1 = Camera(click=onMouse)
    camera1.start()
    
    while True:
        img = camera1.getImage()
        camera1.showImage(img)

if __name__ == '__main__':
    main()

