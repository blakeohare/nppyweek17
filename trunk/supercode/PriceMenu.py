import pygame

from supercode.Util import *

class PriceMenu:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.render_cache = None
	
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
		
		if self.render_cache == None:
			left = 0
			top = 0
			
			self.render_cache = get_image('misc/price_menu_bg').copy()
			
			margin_left = 38
			margin_top = 75
			
			spacing_x = 67
			spacing_y = 80
			
			prices = self.bg.session.prices
			
			x = left + margin_left
			for color in 'red orange yellow lime green aqua blue purple pink brown'.split():
				y = top + margin_top
				for polarity in ('h', 'n', 'v'):
					key = polarity + '_' + color
					price = prices[key]
					img = get_image('boxes/' + key)
					self.render_cache.blit(img, (x + 5, y))
					self.render_cache.blit(get_small_text(format_money(price, False)), (x - 15, y + 32))
					y += spacing_y
				x += spacing_x
			
			img = get_small_text("Left click to raise price. Right click to lower.")
			x = (self.render_cache.get_width() - img.get_width()) // 2
			self.render_cache.blit(img, (x, y))
		
		screen.blit(self.render_cache, (122, 152))