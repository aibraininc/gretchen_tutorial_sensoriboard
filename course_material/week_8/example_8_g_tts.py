#!/usr/bin/env python
import playsound
from gtts import gTTS

def main():
    tts = gTTS('hello hello hello')
    tts.save('hello.mp3')
    playsound.playsound('hello.mp3')

if __name__ == '__main__':
    main()