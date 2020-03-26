#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
def main():
    #We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    #Initalize robot
    robot = Robot()
    #Start robot
    robot.start()
    #TODO Change the values in loopatpoint
    #The parameters are 3d coordinates in the real world
    robot.lookatpoint(0.678253, 0.754351, 0.298137)
    robot.lookatpoint(0, 0, 0.298137)

if __name__ == '__main__':
    print "starting"
    main()
