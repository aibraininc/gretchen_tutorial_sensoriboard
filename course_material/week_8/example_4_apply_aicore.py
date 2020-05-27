#!/usr/bin/env python
import sys
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    #initalize aicore client 
    client = AICoRE()

    # set username
    client.setUserName('Jacob')

    # send text to AICORE
    client.send('What is my favorite food?')

    # get answer from AICORE
    text = client.answer()

if __name__ == '__main__':
    main()
