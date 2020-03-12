#!/usr/bin/env python


import rospy
import roslib

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
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
    #print new_image
    camera1.start()
    #if new_image ==None:
    #    print "nothing"
    #else:
    while(True):
        #print "hello"
        a = camera1.getImage2()
        cv2.imshow("Frame2", a[...,::-1])
        cv2.waitKey(1)

    #test2 = rospy.wait_for_message("/camera/color/image_raw", Image)
    #ew_image = camera1.getImage()
    #cv2.imshow("Frame2", new_image[...,::-1])
    #cv2.waitKey(0)
    #while(True):
    #    new_image = camera1.getImage()
    #    cv2.imshow("Frame2", new_image[...,::-1])
    #    cv2.waitKey(0)
    #    print "outside----------------------"
    #    print type(new_image)
    #    print new_image.shape
    #new_image = camera1.getImage()
    #cv2.imshow("Frame2", new_image[...,::-1])
    #cv2.waitKey(0)

    #image = camera1.getImage()
    #if(image != None):
        #cv2.imshow("Frame2", image[...,::-1])
        #cv2.waitKey(1)
    #while not rospy.is_shutdown():
    #    rospy.spin()



if __name__ == '__main__':
    main()
