import pygame

from supercode.Util import *

_RLEFT = 122
_RTOP = 152

class PriceMenu:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.render_cache = None
		self.plots = None
	
	def process_input(self, events, pressed_keys):
		for event in events:
			
			if event.down:
				click = 0
				if event.action == 'lclick':
					click = 1
				elif event.action == 'rclick':
					click = -1
				
				if click != 0:
					plot = self.get_plot()
					if plot != None:
						self.modify_price(plot[4], click)
						
			if event.down and event.action == 'full':
				self.next = self.bg
				self.bg.next = self.bg
	
	def modify_price(self, key, direction):
		if key.endswith('_all'):
			for color in 'red orange yellow lime green aqua blue purple pink brown'.split():
				self.modify_price(key[:2] + color, direction)
		else:
			price = self.bg.session.prices[key]
			if direction == -1:
				if price > 10:
					price -= 10
			else:
				if price < 200:
					price += 10
			
			self.bg.session.prices[key] = price
			self.render_cache = None
			self.plots = None
			
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
			self.plots = []
			
			margin_left = 38
			margin_top = 75
			
			spacing_x = 55
			spacing_y = 80
			
			prices = self.bg.session.prices
			
			x = left + margin_left
			for color in 'all x red orange yellow lime green aqua blue purple pink brown'.split():
				if color == 'x':
					pygame.draw.rect(self.render_cache, (0, 0, 0), pygame.Rect(x, top + margin_top - 15, 1, spacing_y * 3))
				else:
					y = top + margin_top
					
					for polarity in ('h', 'n', 'v'):
						key = polarity + '_' + color
						
						t = 0
						if color == 'all':
							t += 10
						self.plots.append(
							(x - 20 + t, y - 14, 53, 77, key))
							
						img = get_image('boxes/' + key)
						self.render_cache.blit(img, (x + t, y))
						if color != 'all':
							price = prices[key]
							self.render_cache.blit(get_small_text(format_money(price, False)), (x - 15, y + 32))
						y += spacing_y
				x += spacing_x
			
			img = get_small_text("Left click to raise price. Right click to lower.")
			x = (self.render_cache.get_width() - img.get_width()) // 2
			self.render_cache.blit(img, (x, y))
			
			img = get_small_text("All")
			self.render_cache.blit(img, (margin_left, margin_top - 35))
		
		screen.blit(self.render_cache, (_RLEFT, _RTOP))
		
		plot = self.get_plot()
		if plot != None:
			pygame.draw.rect(
				screen,
				(120, 120, 120),
				pygame.Rect(plot[0] + _RLEFT, plot[1] + _RTOP, plot[2], plot[3]),
				2)
	
	def get_plot(self):
		
		mx = mouse_x() - _RLEFT
		my = mouse_y() - _RTOP
		
		for plot in self.plots:
			if mx >= plot[0] and mx <= plot[0] + plot[2]:
				if my >= plot[1] and my <= plot[1] + plot[3]:
					return plot
		return None
		