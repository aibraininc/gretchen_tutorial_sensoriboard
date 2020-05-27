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

    # TODO: change the values in move
    for i in range(5):
        robot.move(0.0, 1.0)
        time.sleep(0.1)
if __name__ == '__main__':
    main()
