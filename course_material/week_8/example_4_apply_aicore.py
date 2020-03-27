#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    client = AICoRE()

    # set username
    client.setUserName('Wally')

    # send text to AICORE
    client.send('What is my name?')

    # get answer from AICORE
    client.answer()

if __name__ == '__main__':
    main()
