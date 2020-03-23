#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
from example_2_ball_detector import BallDetector
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
camera = Camera()
robot = Robot()


def main():
    ROSEnvironment()
    camera.start()
    robot.start()
    ball_detector = BallDetector()
    cnt = 0

    while True:
        img = camera.getImage()
        (img, centor) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        key = cv2.waitKey(1)
        if key > 0:
            break
        # track ball
        cnt = cnt + 1
        if cnt % 50 == 0:
            print(centor)
            if(centor!= None):
                (x,y,z) = camera.convert2d_3d(centor[0], centor[1])
                print (x,y,z,'on camera axis')
                (x,y,z) = camera.convert3d_3d(x,y,z)
                print (x,y,z,'on robot axis')
                robot.lookatpoint(x,y,z, 4, waitResult = False)

if __name__ == '__main__':
    main()




