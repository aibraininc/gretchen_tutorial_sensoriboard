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
        #TODO: adjust for noise
        r.adjust_for_ambient_noise(source)
        #TODO: listen to source
        audio = r.listen(source)
    #TODO: convert audio to text
    text = r.recognize_google(audio)

    #TODO: send text to client
    client.send(text)
    #TODO: get answer from AICoRe
    answer = client.answer()

    #TODO: Convert text to speech
    tts = gTTS(answer)
    #TODO: Save TTS result
    tts.save('hello.mp3')
    #TODO: Play TTS
    playsound.playsound('hello.mp3')

    #TODO: With recognized text, you can let robot answer.
    print(text)
    if 'hello' in text:
        tts = gTTS('hello hello hello')
        tts.save('hello.mp3')
        playsound.playsound('hello.mp3')


if __name__ == '__main__':
    main()
