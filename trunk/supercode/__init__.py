import pygame
import time
import os
import math
import random

from supercode.TitleScene import TitleScene

class MyEvent:
	def __init__(self, action, down):
		self.action = action
		self.down = down
		self.up = not down

def startgame():
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Super Shop")
	fps = 30
	active_scene = TitleScene()
	counter = 0
	while active_scene != None:
		
		start = time.time()
		
		counter += 1
		
		events = []
		keys_pressed = pygame.key.get_pressed()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				return
			elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
				down = e.type == pygame.KEYDOWN
				action = None
				if e.key == pygame.K_F4:
					if keys_pressed[pygame.K_LALT] or keys_pressed[pygame.K_RALT]:
						return
				elif e.key == pygame.K_UP:
					action = 'up'
				elif e.key == pygame.K_LEFT:
					action = 'left'
				elif e.key == pygame.K_RIGHT:
					action = 'right'
				elif e.key == pygame.K_DOWN:
					action = 'down'
				elif e.key == pygame.K_SPACE:
					action = 'lift'
				
				events.append(MyEvent(action, down))
		
		active_scene.process_input(events)
		active_scene.update(counter)
		active_scene.render(screen, counter)
		
		active_scene = active_scene.next
		
		pygame.display.flip()
		
		end = time.time()
		
		diff = end - start
		
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
	