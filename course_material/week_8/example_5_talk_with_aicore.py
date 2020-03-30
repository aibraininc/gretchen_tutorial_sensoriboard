#!/usr/bin/env python
import sys
import speech_recognition as sr
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    #Initalize AICoRe client
    client = AICoRE()
    #Set up client name
    client.setUserName('Jacob')

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
    #send text to client
    client.send(text)
    #get answer from AICoRe
    client.answer()

if __name__ == '__main__':
    main()
