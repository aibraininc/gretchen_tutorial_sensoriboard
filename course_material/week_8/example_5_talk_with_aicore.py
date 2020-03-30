#!/usr/bin/env python
import sys
import speech_recognition as sr
sys.path.append('..')
from lib.ros_environment import ROSEnvironment
from lib.aicore_client import AICoRE

def main():
    #We need to initalize ROS environment for AICoRE to connect
    ROSEnvironment()
    client = AICoRE()
    client.setUserName('Jacob')

    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    text = r.recognize_google(audio)
    client.send(text)
    client.answer()

if __name__ == '__main__':
    main()


