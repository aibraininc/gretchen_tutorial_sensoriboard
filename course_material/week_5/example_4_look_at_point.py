#!/usr/bin/env python
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

#initalize camera
camera = Camera()
#initalize robot
robot = Robot()

#when mouse is clicked this method is called
def onMouse(event, u, v, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(u,v)
        #convert pixel 2d coordinates to 3d coordiantes on camera axis
        (x,y,z) = camera.convert2d_3d(u,v)
        print (x,y,z,'on camera axis')
        #covert 3d coordinates on camera axis to 3d coordinates on robot axis
        (x,y,z) = camera.convert3d_3d(x,y,z)
        print (x,y,z,'on robot axis')
        #robot to look in the direct of the 3d coordates on robot axis
        robot.lookatpoint(x,y,z, waitResult = False)
        print('look at point end')

def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #starts camera
    camera.start()
    #starts robot
    robot.start()

    #loop
    while True:
        #get image
        img = camera.getImage()
        #show image
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        #Close if key is pressed
        key = cv2.waitKey(1)
        if key >0:
            break

if __name__ == '__main__':
    main()
