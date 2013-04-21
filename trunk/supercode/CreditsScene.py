import pygame

from supercode.JukeBox import *
from supercode.Util import *

class CreditsScene:
	
	def __init__(self):
		self.next = self
	
		self.images = legacy_map(
			lambda x:get_image('credits/credits_' + str(x)),
			range(1, 8))
			
		img = []
		for i in self.images:
			x = pygame.Surface(i.get_size()).convert()
			x.fill((0, 0, 0))
			x.blit(i, (0, 0))
			img.append(x)
		self.images = img
		
		self.counter = 0
	
	def update(self, counter):
		ensure_playing('credits')
		self.counter += 1
	
	def process_input(self, events, pressed):
		for event in events:
			if event.down:
				if event.action == 'pause' or event.action == 'lclick':
					from supercode.TitleScene import TitleScene
					self.next = TitleScene()
	
	def render1(self, screen, counter):
		pass
	
	def render2(self, screen, counter):
		screen.fill((0, 0, 0))
		rate = 3.0
		y = int(screen.get_height() - self.counter * rate)
		
		for img in self.images:
			x = 400 #(screen.get_width() - img.get_width()) // 2
			screen.blit(img, (x, y))
			y += 400
		
		if y - 400 < -img.get_height():
			from supercode.TitleScene import TitleScene
			self.next = TitleScene()
	