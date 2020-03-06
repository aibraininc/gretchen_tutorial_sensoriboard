#!/usr/bin/env python


import rospy
import roslib
from lib.robot import Robot
from lib.camera import Camera
from geometry_msgs.msg import Twist

class System:

    def __init__(self):
        print('Hello')
        self.robot = Robot()
        # self.camera = Camera()
        rospy.Subscriber("/key_vel", Twist, self.keyCallback, queue_size = 10)

    def keyCallback(self, data):
        
        if data.angular.z > 0:
            self.robot.left()
        elif data.angular.z < 0:
            self.robot.right()
        elif data.linear.x > 0:
            self.robot.down()
        elif data.linear.x < 0:
            self.robot.up()

def main():
    rospy.init_node('key_op', anonymous=True)
    system = System()
    while not rospy.is_shutdown():
        rospy.spin()
if __name__ == '__main__':
    main()
