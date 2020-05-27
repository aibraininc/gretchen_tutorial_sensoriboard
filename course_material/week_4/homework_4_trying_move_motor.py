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

    for i in range(10):
        #TODO: change the values in move
        robot.move(0.0, 0.0)
        time.sleep(0.1)
    time.sleep(1) # wait a second
    for i in range(10):
        #TODO: change the values in move
        robot.move(0.0, 0.0)
        time.sleep(0.1)
    for i in range(10):
        #TODO: change the values in move
        robot.move(0.0, 0.0)
        time.sleep(0.1)
    for i in range(10):
        #TODO: change the values in move
        robot.move(0.0, 0.0)
        time.sleep(0.1)

    #TODO: write code to make the robot go up and down
if __name__ == '__main__':
    main()
