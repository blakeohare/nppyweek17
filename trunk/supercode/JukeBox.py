# Playing sounds is in Util.py

import os
import pygame

_now_playing = { 't': None }

def ensure_playing(song):
	
	if _now_playing['t'] != song:
		_now_playing['t'] = song
		path = ('music/' + song + '.ogg').replace('/', os.sep)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play(-1)
