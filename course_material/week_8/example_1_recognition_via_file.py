#!/usr/bin/env python

import speech_recognition as sr
def main():
    #initalize speech recognition
    r = sr.Recognizer()
    #initialize and
    harvard_audio = sr.AudioFile('harvard.wav') # init audio file

    #read audio file
    with harvard_audio as source:
        audio = r.record(source)
    #convert audio to text
    text = r.recognize_google(audio)
    print('result', text)

if __name__ == '__main__':
    main()
