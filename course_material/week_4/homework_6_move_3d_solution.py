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
    time.sleep(2) # wait a second

    # TODO: change the values in lookatpoint for looking at the red square.
    robot.lookatpoint(1,1,1)
    time.sleep(2) # wait a second

    # TODO: change the values in lookatpoint for looking at the green square.
    robot.lookatpoint(1,-1,1)

if __name__ == '__main__':
    main()
