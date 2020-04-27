#!/usr/bin/env python
import sys
import speech_recognition as sr
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

import pygame
import playsound
from gtts import gTTS

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    #Initalize AICoRe client
    client = AICoRE()

    #TODO: Set up client name
    client.setUserName('username')

    #Initalize speeech recogniton
    r = sr.Recognizer()
    #TODO: Initalize mic and set the device_index
    mic = sr.Microphone(device_index=11)
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    text = r.recognize_google(audio)

    client.send(text)
    answer = client.answer()

    #TODO:set the keyword to respond to
    keyword = 
    #check if keyword in input
    if keyword in text:
        #TODO: set a response
        answer = 

    tts = gTTS(answer)
    tts.save('hello.mp3')
    playsound.playsound('hello.mp3')


if __name__ == '__main__':
    main()
