#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ball_detector import BallDetector
from lib.robot import Robot


def main():
    rospy.init_node('camera_show', anonymous=True)
    global robot
    robot = Robot()

    camera1 = Camera()
    camera1.start()
    ball_detector = BallDetector()

    cnt = 0
    while not rospy.is_shutdown():
        img = camera1.getImage()
        (img, centor) = ball_detector.detect(img, 640)
        cv2.imshow("Frame", img[...,::-1])
        cv2.waitKey(1)

        # track ball
        cnt = cnt + 1
        if cnt % 50 == 0:
            (x,y,z) = camera1.convert2d_3d(centor[0], centor[1])
            print (x,y,z,'on camera axis')
            (x,y,z) = camera1.convert3d_3d(x,y,z)
            print (x,y,z,'on robot axis')
            robot.lookatpoint(x,y,z, 1.5, waitResult = False)

if __name__ == '__main__':
    main()

