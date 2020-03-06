#!/usr/bin/env python
import rospy
import roslib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class Camera:

    def __init__(self, callback = None):
        print('Camera')
        self.bridge_ros2cv = CvBridge()
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCallback, queue_size = 1000)
        self.callback = callback
        self.image = None


    def imageCallback(self, image_msg):
        frame = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
        self.image = frame
        if self.callback == None:
            _frame = frame
        else:
            _frame = self.callback(frame)
            frame = _frame
            cv2.imshow("Frame", frame[...,::-1])
            cv2.waitKey(1)