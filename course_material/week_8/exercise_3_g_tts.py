#!/usr/bin/env python
import pygame
import playsound
from gtts import gTTS
tts = gTTS('hello hello hello')
tts.save('hello.mp3')
playsound.playsound('hello.mp3')
