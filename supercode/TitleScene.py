import pygame
from supercode.Util import *

class TitleScene:
	def __init__(self):
		self.next = self
		self.selection = 0
	
	def process_input(self, events):
		for event in events:
			if event.down:
				if event.action == 'up':
					self.selection -= 1
				elif event.action == 'down':
					self.selection += 1
				elif event.action == 'lift':
					self.do()
			
			if self.selection < 0:
				self.selection = 0
			elif self.selection >= 5:
				self.selection = 4
	
	def do(self):
		pass
	
	def update(self, counter):
		pass
	
	def render(self, screen, render_counter):
		screen.blit(get_image('title/bg.png'), (0, 0))
		city = get_image('title/skyline.png')
		screen.blit(city, (0, screen.get_height() - city.get_height()))
		character = get_image('title/character.png')
		capes = legacy_map(lambda x:get_image('title/cape_' + str(x)), range(1, 6))
		capes = capes + capes[:len(capes) - 1][::-1]
		cape = capes[(render_counter // 1) % len(capes)]
		
		screen.blit(cape, (614, 277))
		screen.blit(character, (596, 259))
		
		screen.blit(get_image('title/words.png'), (52, 60))
		
		screen.blit(get_image('title/speech.png'), (225, 207))
		
		x = 290
		y = 230
		i = 0
		choice_key = ['tutorial', 'play', 'options', 'credits', 'quit']
		blot = get_image('title/blot.png')
		for choice in choice_key:
			screen.blit(get_image('title/option_' + choice), (x, y))
			
			if i == self.selection:
				screen.blit(blot, (x - blot.get_width() - 8, y - 5))
			
			x += 20
			y += 43
			i += 1
		