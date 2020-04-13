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
    #Initalize mic
    mic = sr.Microphone()
    with mic as source:
        #adjust for noise
        r.adjust_for_ambient_noise(source)
        #listen to source
        audio = r.listen(source)
    #convert audio to text
    text = r.recognize_google(audio)

    #TODO: With recognized text, you can let robot answer.
    print(text)
    if 'hello' in text:
        tts = gTTS('hello hello hello')
        tts.save('hello.mp3')
        playsound.playsound('hello.mp3')
        
    
if __name__ == '__main__':
    main()
