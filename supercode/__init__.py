import pygame
import time
import os
import math
import random

from supercode.InputConfigMenu import get_scheme
from supercode.TitleScene import TitleScene

SHOW_FPS = True

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
		
		input = get_scheme()
		
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
				if e.key == pygame.K_w:
					if keys_pressed[pygame.K_LCTRL] or keys_pressed[pygame.K_RCTRL]:
						return
				if e.key == pygame.K_F4:
					if keys_pressed[pygame.K_LALT] or keys_pressed[pygame.K_RALT]:
						return
				
				if e.key == pygame.K_ESCAPE or e.key == pygame.K_SPACE or e.key == pygame.K_RETURN:
					action = 'pause'
				
				# arrow keys will ALWAYS work
				if e.key == pygame.K_UP:
					action = 'up'
				elif e.key == pygame.K_LEFT:
					action = 'left'
				elif e.key == pygame.K_RIGHT:
					action = 'right'
				elif e.key == pygame.K_DOWN:
					action = 'down'
				
				# r and t are used in all layouts
				if e.key == pygame.K_r:
					action = 'menu' # price
				elif e.key == pygame.K_t:
					action = 'order' # reorder
				
				
				if input == 'dvorak':
					if e.key == pygame.K_a:
						action = 'left'
					elif e.key == pygame.K_o:
						action = 'down'
					elif e.key == pygame.K_e:
						action = 'right'
					elif e.key == pygame.K_COMMA:
						action = 'up'
					elif e.key == pygame.K_PERIOD:
						action = 'full'
					elif e.key == pygame.K_QUOTE:
						action = 'single'
				elif input == 'qwerty':
					if e.key == pygame.K_w:
						action = 'up'
					elif e.key == pygame.K_a:
						action = 'left'
					elif e.key == pygame.K_s:
						action = 'down'
					elif e.key == pygame.K_d:
						action = 'right'
					elif e.key == pygame.K_e:
						action = 'full'
					elif e.key == pygame.K_q:
						action = 'single'
				elif input == 'arrows':
					if e.key == pygame.K_s:
						action = 'single'
					elif e.key == pygame.K_f:
						action = 'full'
				
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
		
		
		if SHOW_FPS:
			if diff == 0:
				vfps = "Fast"
			else:
				vfps = str(int(1.0 / diff))
			
			pygame.display.set_caption("FPS: " + vfps)
		
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
	