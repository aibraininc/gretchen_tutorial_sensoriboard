#!/usr/bin/env python
import rospy
import roslib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class Camera:

    def __init__(self):
        print('Camera Initialized')
        self.bridge_ros2cv = CvBridge()
        self.image = None
        while self.image is None:
            try:
                self.image = rospy.wait_for_message("/camera/color/image_raw", Image)
            except:
                pass
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCallback, queue_size = 1000)




    def imageCallback(self, image_msg):
        print("Recieved Image")
        frame = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
        self.image = frame
        #cv2.imshow("Frame", frame[...,::-1])
        #cv2.waitKey(1)

    def getImage(self):
        cv2.imshow("Frame", self.image[...,::-1])
        cv2.waitKey(1)
