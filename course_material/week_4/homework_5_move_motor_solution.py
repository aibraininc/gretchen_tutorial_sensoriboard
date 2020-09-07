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
    robot.move(0.5,0.1)
    time.sleep(1) # wait a second

    #TODO: remember current position
    print ("Pan angle is ",robot.getPosition()[0], "Tilt angle is", robot.getPosition()[1])
    current_pan = robot.getPosition()[0]
    current_tilt = robot.getPosition()[1]

    #TODO: look somewhere els other than current position
    robot.move(-0.3,-0.3)
    time.sleep(1) # wait a second

    #TODO: return back to looking at the point you remember
    robot.move(current_pan, current_tilt)
    time.sleep(1) # wait a second

if __name__ == '__main__':
    main()
