#!/usr/bin/env python
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment

#initalize camera
camera = Camera()
#initalize robot
robot = Robot()


def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #start camera
    camera.start()
    #start robot
    robot.start()
    #initalize ball detector
    ball_detector = BallDetector()
    #count
    cnt = 0

    #loop
    while True:
        #get image from camera
        img = camera.getImage()

        (img, center) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break
        # track ball
        cnt = cnt + 1
        if cnt % 50 == 0:
            print(center)
            if(center!= None):
                #converts 2d coordinates to 3d coordinates on camera axis
                (x,y,z) = camera.convert2d_3d(center[0], center[1])
                print (x,y,z,'on camera axis')
                #converts 3d coordinates on camera axis to 3d coordinates on robot axis
                (x,y,z) = camera.convert3d_3d(x,y,z)
                print (x,y,z,'on robot axis')
                #move robot to look at 3d point 
                robot.lookatpoint(x,y,z, 4, waitResult = False)

if __name__ == '__main__':
    main()
