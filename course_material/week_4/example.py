#!/usr/bin/env python
import rospy
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
def main():
    ROSEnvironment()
    robot1 = Robot()
    robot1.start()
    #robot1.move(-0.5, 0.1)
    robot1.lookatpoint(0.678253, 0.754351, 0.298137)
    robot1.lookatpoint(0, 0, 0.298137)

    #robot1.move(1.5, 0.1)
    #while not rospy.is_shutdown():
    #    continue
if __name__ == '__main__':
    print "starting"
    main()
