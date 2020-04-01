#!/usr/bin/env python
import pygame
from gtts import gTTS
tts = gTTS('hello')
tts.save('hello.mp3')

