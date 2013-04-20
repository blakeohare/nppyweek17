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
	r_screen = pygame.display.set_mode((1000, 700))
	v_screen = pygame.Surface((500, 350)).convert()
	pygame.display.set_caption("Super Shop")
	fps = 30
	active_scene = TitleScene()
	counter = 0
	pressed_keys = {}
	while active_scene != None:
		
		start = time.time()
		
		counter += 1
		
		events = []
		keys_pressed = pygame.key.get_pressed()
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				return
			elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
				down = e.type == pygame.MOUSEBUTTONDOWN
				action = None
				if e.button == 1:
					action = 'lclick'
				elif e.button == 3:
					action = 'rclick'
				
				events.append(MyEvent(action, down))
				
			elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
				down = e.type == pygame.KEYDOWN
				action = None
				if e.key == pygame.K_F4:
					if keys_pressed[pygame.K_LALT] or keys_pressed[pygame.K_RALT]:
						return
				elif e.key == pygame.K_ESCAPE:
					return
				elif e.key == pygame.K_UP:
					action = 'up'
				elif e.key == pygame.K_LEFT:
					action = 'left'
				elif e.key == pygame.K_RIGHT:
					action = 'right'
				elif e.key == pygame.K_DOWN:
					action = 'down'
				elif e.key == pygame.K_s:
					action = 'single'
				elif e.key == pygame.K_f:
					action = 'full'
				elif e.key == pygame.K_SPACE or e.key == pygame.K_RETURN:
					action = 'lift'
				elif e.key == pygame.K_r:
					action = 'menu'
				elif e.key == pygame.K_t:
					action = 'order'
				
				if action != None:
					events.append(MyEvent(action, down))
		
		for event in events:
			pressed_keys[event.action] = event.down
		
		active_scene.process_input(events, pressed_keys)
		active_scene.update(counter)
		active_scene.render1(v_screen, counter)
		pygame.transform.scale(v_screen, (1000, 700), r_screen)
		active_scene.render2(r_screen, counter)
		
		active_scene = active_scene.next
		
		
		pygame.display.flip()
		
		end = time.time()
		
		diff = end - start
		
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
	