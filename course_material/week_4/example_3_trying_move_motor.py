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
    #move takes in pan and tilt value of the motor
    #can be from 0.0 to 1.0
    #TODO change the values in move
    while(True):
        robot.move(0, 0)


if __name__ == '__main__':
    print "starting"
    main()
