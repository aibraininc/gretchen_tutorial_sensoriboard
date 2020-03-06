#!/usr/bin/env python

import time
import rospy
import roslib
import cv2
from lib.robot import Robot
from lib.camera import Camera
from lib.ball_detector import BallDetector
from lib import common
import numpy as np

class BallTrackingSystem:

    def __init__(self):
        self.initParam()
        self.pan_speed = 0
        self.tilt_speed = 0
        self.latestImage = None

        # init 
        self.robot = Robot()
        self.ball_detector = BallDetector()
        self.camera = Camera()

    def initParam(self):
        self.rate = rospy.get_param("~rate", 20)

        # Joint speeds are given in radians per second
        self.max_joint_speed = rospy.get_param('~max_joint_speed', 0.1)

        # The pan/tilt thresholds indicate what percentage of the image window
        # the ROI needs to be off-center before we make a movement
        self.pan_threshold = rospy.get_param("~pan_threshold", 0.05)
        self.tilt_threshold = rospy.get_param("~tilt_threshold", 0.05)
        
        # The gain_pan and gain_tilt parameter determine how responsive the
        # servo movements are. If these are set too high, oscillation can result.
        self.gain_pan = rospy.get_param("~gain_pan", 1.0)
        self.gain_tilt = rospy.get_param("~gain_tilt", 1.0)

        self.max_pan_angle_radian = rospy.get_param("~max_pan_angle_radian", 1.0)
        self.max_tilt_angle_radian = rospy.get_param("~max_tilt_angle_radian", 1.0)


    def set_speed(self, percent_offset_x, percent_offset_y):
        if abs(percent_offset_x) > self.pan_threshold:
            if percent_offset_x > 0:
                self.pan_speed = min(self.max_joint_speed, max(0, self.gain_pan * abs(percent_offset_x)))
            else:            
                self.pan_speed = -1 *min(self.max_joint_speed, max(0, self.gain_pan * abs(percent_offset_x)))
        else:
            self.pan_speed = 0

        if abs(percent_offset_y) > self.tilt_threshold:
            if percent_offset_y > 0:
                self.tilt_speed = min(self.max_joint_speed, max(0, self.gain_tilt * abs(percent_offset_y)))
            else:            
                self.tilt_speed = -1 *min(self.max_joint_speed, max(0, self.gain_tilt * abs(percent_offset_y)))
        else:
            self.tilt_speed = 0
        return (self.pan_speed, self.tilt_speed)




def main():
    system = BallTrackingSystem()
    while not rospy.is_shutdown():
        # delay 0.1s
        common.sleep(0.1) 

        # get camera image and detect object
        currentImage = system.camera.image 
        if type(currentImage) != np.ndarray:
            continue
        results =  system.ball_detector.detect(currentImage, 640)
        detectedResultImage = results[0]
        ball = results[1]
        
        if ball != None:
            # ball position is x,y on image. 
            # x and y are between -1 and 1.
            ball_position = system.ball_detector.optimized(ball, detectedResultImage)

            # print ball postion.
            print("ball_position")
            print(ball_position)

            # do controll motor yourself
            if ball_position[0] > 0.1:
                system.robot.right(0.08)
            elif ball_position[0] < -0.1:
                system.robot.left(0.08)

            # set speed of robot head with ball postion
            # (pan_speed, tilt_speed) = system.set_speed(ball_position[0], ball_position[1])
            # system.robot.move(pan_speed, tilt_speed)

        # show detected object
        cv2.imshow("detect result", detectedResultImage[...,::-1])
        cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('ball_tracking', anonymous=True)
    main()
