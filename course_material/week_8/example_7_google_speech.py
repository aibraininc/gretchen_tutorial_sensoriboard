#!/usr/bin/env python
from google_speech import Speech # it is only on python 3

def main():
    text = "How are you?"
    lang = "en"
    speech = Speech(text, lang) # set text, language
    speech.play() # play text

if __name__ == '__main__':
    main()