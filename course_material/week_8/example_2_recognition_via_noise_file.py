#!/usr/bin/env python

import speech_recognition as sr
def main():
    #initalize speech recogniton
    r = sr.Recognizer() # init recognizer
    #initalize audio file
    jackhammer_audio = sr.AudioFile('jackhammer.wav')

    with jackhammer_audio as source:
        #remove noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        #read audio
        audio = r.record(source)
    #recognize speech
    text = r.recognize_google(audio)
    print('result', text)

if __name__ == '__main__':
    main()
