#!/usr/bin/env python

import pyttsx

def main():
    voiceEngine = pyttsx.init()
    newVoiceRate = 120 # the rate of voice
    voiceEngine.setProperty('rate', newVoiceRate)
    voiceEngine.say('I am jacob.')
    voiceEngine.runAndWait()

if __name__ == '__main__':
    main()