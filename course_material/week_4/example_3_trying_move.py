#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.robot import Robot
from lib.ros_environment import ROSEnvironment
def main():
    ROSEnvironment()
    robot1 = Robot()
    robot1.start()
    robot1.lookatpoint(0.678253, 0.754351, 0.298137)
    robot1.lookatpoint(0, 0, 0.298137)

if __name__ == '__main__':
    print "starting"
    main()
