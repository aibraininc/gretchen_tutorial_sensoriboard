#!/usr/bin/env python


import rospy
import roslib
import sys
import cv2
from control_msgs.msg import PointHeadAction, PointHeadGoal
import actionlib

sys.path.append('..')

from lib.camera import Camera
#include <geometry_msgs/PointStamped.h>
#include <control_msgs/PointHeadAction.h>


def main():
    rospy.init_node('camera_show', anonymous=True)
    camera1 = Camera()
    image = camera1.getImage()
    if(image != None):
        cv2.imshow("Frame2", image[...,::-1])
        cv2.waitKey(1)
    while not rospy.is_shutdown():
        rospy.spin()



if __name__ == '__main__':
    main()
