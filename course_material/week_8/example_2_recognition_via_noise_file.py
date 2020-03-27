#!/usr/bin/env python

import speech_recognition as sr

def main():
    r = sr.Recognizer() # init recognizer
    harvard = sr.AudioFile('jackhammer.wav') # init audio file
    with harvard as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source)
    text = r.recognize_google(audio)
    print('result', text)

if __name__ == '__main__':
    main()