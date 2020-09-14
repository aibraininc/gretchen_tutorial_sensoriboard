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

    #List all the microphone hardware
    for i, item in enumerate(sr.Microphone.list_microphone_names()):
        print( i, item)

    #TODO: Initalize mic and set the device_index
    mic = sr.Microphone(device_index=1)

    print "I'm listening"
    
    with mic as source:
        #TODO: adjust for noise
        
        #TODO: listen to source
        audio = 
    #TODO: convert audio to text
    text =

    #TODO: send text to client
    
    #TODO: get answer from AICoRe
    answer = 

    #TODO: Convert text to speech
    tts = 
    #TODO: Save TTS result
    
    #TODO: Play TTS
    

        
    
if __name__ == '__main__':
    main()
