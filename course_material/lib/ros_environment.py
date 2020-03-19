import rospy
import roslib


class ROSEnvironment:
    def __init__(self):
        print('ROS Enviornment Started')
        rospy.init_node('ros_node', anonymous=True)
