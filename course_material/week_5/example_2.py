#!/usr/bin/env python


import rospy
import roslib
import sys
from control_msgs.msg import PointHeadAction, PointHeadGoal
import actionlib

sys.path.append('..')

from lib.robot import Robot
#include <geometry_msgs/PointStamped.h>
#include <control_msgs/PointHeadAction.h>

class client:

    def __init__(self):

        self.robot = Robot()
        #rospy.Timer(rospy.Duration(1.0), self.robotUpdate)

    def robotUpdate(self, event):
        # self.robot.test()
        self.robot.move(0, 0)

def main():
    rospy.init_node('ball_tracking', anonymous=True)
    head_client = actionlib.SimpleActionClient("/head_controller/absolute_point_head_action", PointHeadAction)
    head_client.wait_for_server()
    goal = PointHeadGoal()
    goal.target.header.stamp = rospy.Time.now()
    goal.target.header.frame_id = "/camera_color_optical_frame"
    goal.pointing_axis.x = 0
    goal.pointing_axis.y = 0
    goal.pointing_axis.z = 1

    goal.target.point.x = 0.7
    goal.target.point.y = 0
    goal.target.point.z = 0.4
    goal.max_velocity = 0.1
    goal.min_duration = rospy.Duration(2.0)
    head_client.send_goal(goal)
    head_client.wait_for_result()
    #while not rospy.is_shutdown():
    #    rospy.spin()
if __name__ == '__main__':
    main()
