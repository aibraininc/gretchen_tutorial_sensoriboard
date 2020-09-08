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

    
    time.sleep(1) # wait a second

    #TODO: remember current position
    curr_pos = 
    curr_pan = 
    curr_tilt = 

    #TODO: look somewhere else other than current position
    robot.move(,)
    time.sleep(1) # wait a second

    #TODO: return back to the current position 
    robot.move(,)
    time.sleep(1) # wait a second

if __name__ == '__main__':
    main()
