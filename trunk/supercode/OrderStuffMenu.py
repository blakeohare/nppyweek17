from supercode.Session import *
from supercode.Util import *

class OrderStuffMenu:
	def __init__(self, bg):
		self.bg = bg
		self.next = self
		self.cache = None
		self.close_plot = None
		self.plots = []
	
	def update(self, counter):
		pass
	
	def process_input(self, events, pressed):
		for event in events:
			if event.down:
				if event.action == 'lclick':
					if is_over_plot(self.close_plot):
						self.next = self.bg
						self.bg.next = self.bg
					elif self.plots != None:
						for plot in self.plots:
							if is_over_plot(plot):
								self.next = self.bg
								self.bg.next = self.bg
								self.bg.session.order_more(plot[4])
	
	def render1(self, screen, counter):
		self.bg.render1(screen, counter)
	
	def render2(self, screen, counter):
		self.bg.render2(screen, counter)
		
		_LEFT = 122
		_TOP = 159
		if self.cache == None:
			cache = get_image('misc/price_menu_bg').copy()
			
			cb = get_image('misc/close_button')
			x = cache.get_width() - cb.get_width() - 25
			y = 25
			self.close_plot = (x + _LEFT, y + _TOP, cb.get_width(), cb.get_height())
			
			cache.blit(cb, (x, y))
			
			line1 = get_text("Cost per item: $50")
			line2 = get_text("Items per palette: 15 ($750)")
			line3 = get_small_text("(5 hero, 5 villain, 5 neutral)")
			
			lines = [line1, line2, line3, get_small_text(' '), get_text("ORDER:")]
			
			x = 35
			y = 28
			for line in lines:
				cache.blit(line, (x, y))
				y += line.get_height() + 20
			plots = []
			i = 0
			for color in [:self.bg.session.spectrum_available]:
				px = i * 64 + 45
				j = 0
				for prefix in 'vhn':
					img = get_image('boxes/' + prefix + "_" + color)
					py = y + 30 - j * 8
					cache.blit(img, (px + 12, py + 11))
					j += 1
				i += 1
				
				plots.append((px + _LEFT, py + _TOP, 40, 60, color))
			self.plots = plots
				
			
			self.cache = cache
		
		
		screen.blit(self.cache, (_LEFT, _TOP))
		
		if is_over_plot(self.close_plot):
			for candy in 'yum':
				screen.blit(get_image('misc/close_button'), self.close_plot[:2])
		else:
			for plot in self.plots:
				if is_over_plot(plot):
					pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(plot[0], plot[1], plot[2], plot[3]), 2)
					break
				