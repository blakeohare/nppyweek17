import pygame

from supercode.InputConfigMenu import *
from supercode.IntroSlideshow import *
from supercode.JukeBox import *
from supercode.PlayScene import *
from supercode.Util import *

class TitleScene:
	def __init__(self):
		self.next = self
		self.selection = 0
		self.choice_keys = ['play', 'tutorial', 'options', 'credits', 'quit']
		self.bg_cache = None
		
	def process_input(self, events, pressed_keys):
		for event in events:
			if event.down:
				if event.action == 'up':
					self.selection -= 1
				elif event.action == 'down':
					self.selection += 1
				elif event.action == 'pause':
					self.do()
			
			if self.selection < 0:
				self.selection = 0
			elif self.selection >= 5:
				self.selection = 4
	
	def do(self):
		# POLISH: transition scenes
		key = self.choice_keys[self.selection]
		if key == 'quit':
			self.next = None
		elif key == 'play':
			self.next = PlayScene()
		elif key == 'tutorial':
			self.next = IntroSlideshow()
		elif key == 'options':
			self.next = InputConfigMenu()
		elif key == 'credits':
			self.next = CreditsScene()
		else:
			pass # This shouldn't happen
	
	def update(self, counter):
		ensure_playing('title')
	
	def render1(self, screen, render_counter):
		# render at full resolution
		pass
	
	def render2(self, screen, render_counter):
		
		if self.bg_cache == None:
			self.bg_cache = screen.copy()
			bg_slice = get_image('title/bg_slice.png')
			t = pygame.Surface((25, 700))
			for i in range(25):
				t.blit(bg_slice, (i, 0))
			for i in range(0, 1000, 25):
				self.bg_cache.blit(t, (i, 0))
			city = get_image('title/skyline.png')
			self.bg_cache.blit(city, (0, screen.get_height() - city.get_height()))
			self.bg_cache.blit(get_image('title/words.png'), (78, 61))
			self.bg_cache.blit(get_image('title/speech.png'), (278, 243))
		
		screen.blit(self.bg_cache, (0, 0))
		
		character = get_image('title/character.png')
		capes = legacy_map(lambda x:get_image('title/cape_' + str(x)), range(1, 6))
		capes = capes + capes[1:len(capes) - 1][::-1]
		cape = capes[(render_counter // 3) % len(capes)]
		
		t = 3
		screen.blit(cape, (768, 318 + t))
		screen.blit(character, (753, 300 + t))
		
		
		
		x = 363
		y = 272
		i = 0
		
		blot = get_image('title/blot.png')
		for choice in self.choice_keys:
			screen.blit(get_image('title/option_' + choice), (x, y))
			
			if i == self.selection:
				screen.blit(blot, (x - blot.get_width() - 8, y - 5))
			
			x += 25
			y += 44
			i += 1
		
		#pygame.transform.scale(screen, r_screen.get_size(), r_screen)