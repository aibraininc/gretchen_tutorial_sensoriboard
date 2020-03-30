#!/usr/bin/env python

import speech_recognition as sr
#initalize speech recognition
r = sr.Recognizer()
#initialize and
harvard_audio = sr.AudioFile('harvard.wav') # init audio file

#read audio file
with harvard_audio as source:
    audio = r.record(source)
text = r.recognize_google(audio)
print('result', text)
