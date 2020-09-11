#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
import time

def startNod(robot):
    robot.center()
    time.sleep(1)

    #TODO: insert code to make the robot nod.

def startShake(robot):
    robot.center()
    time.sleep(1)

    #TODO: insert code to make the robot shake.


def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize robot
    robot = Robot()
    # Start robot
    robot.start()
    startNod(robot)
    # Uncomment/comment  
    startNod(robot)
    # Uncomment/comment 
    # startShake(robot)


if __name__ == '__main__':
    main()
