#!/usr/bin/env python
from google_speech import Speech # it is only on python 3
text = "How are you?"
lang = "en"
speech = Speech(text, lang) # set text, language
speech.play() # play text