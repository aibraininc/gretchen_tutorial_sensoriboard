#!/usr/bin/env python

# whenever you say a object, robot looks at the object.

import threading
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# STT
import speech_recognition as sr
import cv2
import argparse
import numpy as np
print(cv2.__version__)
sys.path.append('..')

# TTS
import pygame
import playsound
from gtts import gTTS

sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')
import rospy
# Can add gretchen lib
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE
from lib.camera_v2 import Camera
from lib.robot import Robot

def main():
    ROSEnvironment()
    camera = Camera()
    camera.start()
    robot = Robot()
    robot.start()

    #loops
    while(True):
        #gets image from camera
        cam_image = camera.getImage()
        cv2.imshow("Image", cam_image)
        key = cv2.waitKey(1)
        if key > 0:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
