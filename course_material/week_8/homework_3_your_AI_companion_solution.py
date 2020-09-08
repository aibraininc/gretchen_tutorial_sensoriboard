#!/usr/bin/env python
import sys
import speech_recognition as sr
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE
from lib.robot import Robot

import pygame
import playsound
from gtts import gTTS
import time



def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()

    # Start robot
    robot = Robot()
    robot.start()

    #Initalize AICoRe client
    client = AICoRE()


    #TODO: Set up client name
    client.setUserName('username')

    #Initalize speeech recogniton
    r = sr.Recognizer()

    #List all the microphone hardware
    for i, item in enumerate(sr.Microphone.list_microphone_names()):
        print( i, item)

    #TODO: Initalize mic and set the device_index
    mic = sr.Microphone(device_index=7)
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    text = r.recognize_google(audio)

    client.send(text)
    answer = client.answer()

    tts = gTTS(answer)
    tts.save('answer.mp3')
    playsound.playsound('answer.mp3')

    #TODO: check if 'yes' in voice input
    if 'yes.' in answer.lower():
        #TODO: robot should nod
        startNod(robot)

    #TODO: check if 'no' in voice input
    elif 'no.' in answer.lower():
        #TODO: robot should shake
        startShake(robot)

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


if __name__ == '__main__':
    main()
