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
    robot.up(1)
    for i in range(0,3):
        robot.down(2)
        time.sleep(0.5)

        robot.up(2)
        time.sleep(0.5)
    robot.center()

def startShake(robot):
    robot.center()
    time.sleep(1)

    #TODO: insert code to make the robot nod.
    robot.left(1)
    for i in range(0,3):
        robot.right(2)
        time.sleep(0.5)

        robot.left(2)
        time.sleep(0.5)
    robot.center()


def main():
    # We need to initalize ROS environment for Robot and camera to connect/communicate
    ROSEnvironment()
    # Initalize robot
    robot = Robot()
    # Start robot
    robot.start()
    # Uncomment/comment  
    startNod(robot)
    # Uncomment/comment 
    # startShake(robot)


if __name__ == '__main__':
    main()
