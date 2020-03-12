#!/usr/bin/env python
import rospy
import roslib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import copy

class Camera:

    def __init__(self):
        print('Camera Initialized')
        self.bridge_ros2cv = CvBridge()
        self.image = None
        while self.image is None:
            try:
                image_msg = rospy.wait_for_message("/camera/color/image_raw", Image)
                self.image = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
                #print type(self.image)
                #print self.image.shape
                print "check 1"
            except:
                pass
        #rospy.Subscriber("/camera/color/image_raw", Image, self.imageCallback, queue_size = 1)
        #rospy.Subscriber("/camera/color/image_raw", Image, self.getImage, queue_size = 1000)

        #rospy.Timer(rospy.Duration(1.0/5.0), self.getImage)

    def start(self):
        rospy.init_node('camera_show', anonymous=True)
        #while not rospy.is_shutdown():
        #    rospy.spin()

    def imageCallback(self, image_msg):
        print("Recieved Image")
        print "check 2"

        frame = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
        print type(frame)
        print frame.shape
        self.image = frame
        #self.getImage(self.image)
        #cv2.imshow("asdf", self.image[...,::-1])
        #cv2.waitKey(1)
    def getImage2(self):
        try:
            image_msg = rospy.wait_for_message("/camera/color/image_raw", Image)
            self.image = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
                #print type(self.image)
                #print self.image.shape
            print "got something"
        except:
            pass
        return self.image
    def getImage(self, event):
        #return image
        print "check 3"
        print "returning latest image"
        #return self.image
        cv2.imshow("getimage", self.image[...,::-1])
        cv2.waitKey(1)
    def __getitem__(self, item):
        #return image
        return self.image[item]
