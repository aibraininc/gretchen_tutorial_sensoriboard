#!/usr/bin/env python
import speech_recognition as sr

def main():
    r = sr.Recognizer()
    mic = sr.Microphone() # use default mic, now it occurs errors.
    with mic as source:
        r.adjust_for_ambient_noise(source) # adjust noise
        audio = r.listen(source)
    print('Hello')
    text = r.recognize_google(audio)
    print('result', text)

if __name__ == '__main__':
    main()