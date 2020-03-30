#!/usr/bin/env python
import pyttsx
text = "How are you?"
engine = pyttsx.init() 
engine.say(text)
engine.runAndWait() # run tts
print('end')
