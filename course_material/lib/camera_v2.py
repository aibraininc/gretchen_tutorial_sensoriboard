#!/usr/bin/env python
import rospy
import roslib
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


from geometry_msgs.msg import PointStamped
import tf


class Camera:

    def __init__(self, callback = None, click = None):
        print('Camera')
        self.bridge_ros2cv = CvBridge()
        rospy.Subscriber("/camera/color/image_raw", Image, self.imageCallback, queue_size = 1000)
        self.callback = callback
        self.click = click
        self.image = None
        self.listener = None
        self.click_x = 0
        self.click_y = 0



    def start(self):
        print("starting camera")
        #rospy.init_node('camera_show', anonymous=True)
        msg=rospy.wait_for_message('/camera/color/camera_info', CameraInfo)        
        # print(msg)

        self.fx = msg.K[0]
        self.fy = msg.K[4]
        self.cx = msg.K[2]
        self.cy = msg.K[5]
        self.listener = tf.TransformListener()
        self.listener.waitForTransform("/base_link", "/camera_color_optical_frame", rospy.Time(0),rospy.Duration(4.0))


    def convert2d_3d(self, u,v):
        x =  ( u  - self.cx )/ self.fx
        y =  ( v  - self.cy )/ self.fy
        z = 1.0
        return (x,y,z)

    def convert_3d_2d(self,x,y,z):
        # 3d point on camera -> 2d point on camera
        u = self.fx * x + self.cx
        v = self.fy * y + self.cy

    def convert3d_3d(self,x,y,z):
        # point from camera -> point from base
        cam_point = PointStamped()
        cam_point.header.frame_id = "/camera_color_optical_frame"
        cam_point.header.stamp = rospy.Time(0)
        cam_point.point.x = x
        cam_point.point.y = y
        cam_point.point.z = z
        self.listener.waitForTransform("/base_link", "/camera_color_optical_frame", rospy.Time(0),rospy.Duration(4.0))
        p = self.listener.transformPoint("/base_link", cam_point)
        return (p.point.x,p.point.y,p.point.z)

    def showImage(self, frame, frame_name = 'Frame'):
        cv2.imshow(frame_name, frame[...,::-1])
        cv2.setMouseCallback(frame_name, self.onMouse)
        cv2.waitKey(1)

    def onMouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.click is not None:
                self.click(self,x,y)
            self.click_x = x
            self.click_y = y

    def imageCallback(self, image_msg):
        frame = self.bridge_ros2cv.imgmsg_to_cv2(image_msg, desired_encoding="passthrough")
        self.image = frame
        if self.callback == None:
            _frame = frame
        else:
            _frame = self.callback(frame)
            frame = _frame

    def getClickPoint(self):
        return(self.click_x,self.click_y)
    def getImage(self):
        return self.image
        

        
