#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
import time

def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize robot
    robot = Robot()
    # Start robot
    robot.start()
    
    robot.center()
    time.sleep(1)

    #TODO: change the values in left
    robot.left(0.2)
    time.sleep(1)#wait a second

    #TODO: change the values in right
    robot.right(0.2)
    time.sleep(1)

    #TODO make the robot move up, down

if __name__ == '__main__':
    main()
