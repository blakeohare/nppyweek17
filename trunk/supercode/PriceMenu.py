import pygame

from supercode.Util import *

class PriceMenu:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
	
	def process_input(self, events, pressed_keys):
		for event in events:
			if event.down and event.action == 'full':
				self.next = self.bg
				self.bg.next = self.bg
				
	def update(self, counter):
		self.bg.update(counter)
	
	def render1(self, screen, counter):
		self.bg.render1(screen, counter)
	
	def render2(self, screen, counter):
		self.bg.render2(screen, counter)
		
		#pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, 20, 20, 20))
		screen.blit(get_image('misc/price_menu_bg'), (122, 152))
	