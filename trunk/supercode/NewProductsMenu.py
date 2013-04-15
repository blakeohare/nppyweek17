from supercode.Products import *
from supercode.Util import *

class NewProductsMenu:
	def __init__(self, bg, color):
		self.bg = bg
		self.next = self
		self.color = color
		self.render_cache = None
		self.keys = ['h_' + color, 'v_' + color, 'n_' + color]
		self.forwhom = ["For Heroes", "For Villains", "For Anyone"]
		self.index = 0
		self.close_button_plot = None
		self.prev_plot = None
		self.next_plot = None
		
	
	def update(self, counter):
		pass
	
	def process_input(self, events, pressed_keys):
		for event in events:
			if event.action == 'lclick' and event.down:
				if is_over_plot(self.close_button_plot):
					self.next = self.bg
					self.bg.next = self.bg
				if is_over_plot(self.prev_plot) and self.index > 0:
					self.index -= 1
					self.render_cache = None
				if is_over_plot(self.next_plot) and self.index < 2:
					self.index += 1
					self.render_cache = None
					
	
	
	def render1(self, screen, counter):
		self.bg.render1(screen, counter)
	
	def render2(self, screen, counter):
		self.bg.render2(screen, counter)
		
		_LEFT = 122
		_TOP = 159
		
		if self.render_cache == None:
			
			title, description = get_product(self.keys[self.index])
			
			rc = get_image('misc/radio_announce').copy()
			
			self.close_button_plot
			cb = get_image('misc/close_button')
			close_x = rc.get_width() - cb.get_width() - 25
			close_y = 25
			rc.blit(cb, (close_x, close_y))
			self.close_button_plot = (close_x + _LEFT, close_y + _TOP, cb.get_width(), cb.get_height())
			
			line1 = get_text("New Stuff " + self.forwhom[self.index] + "!")
			line2 = get_text(title)
			lines = legacy_map(get_small_text, description)
			
			left_margin = 45
			line_spacing = 20
			y = 45
			rc.blit(line1, (left_margin, y))
			y += line1.get_height() + line_spacing
			rc.blit(line2, (left_margin, y))
			y += line2.get_height() + line_spacing
			
			for img in lines:
				
				rc.blit(img, (left_margin + 10, y))
				y += img.get_height() + 13
			
			arrow_label = get_text("Item " + str(self.index + 1) + " of 3")
			
			rc.blit(arrow_label, (300, 335))
			
			self.render_cache = rc
		
		screen.blit(self.render_cache, (_LEFT, _TOP))
		
		left_blinks = self.index > 0
		right_blinks = self.index < 2
		left_arrow = get_arrow('left', left_blinks, counter)
		right_arrow = get_arrow('right', right_blinks, counter)
		
		lx = _LEFT + 570
		y = _TOP + 319
		rx = _LEFT + 630
		
		self.prev_plot = [lx, y, left_arrow.get_width(), left_arrow.get_height()]
		self.next_plot = [rx, y, right_arrow.get_width(), right_arrow.get_height()]
		
		screen.blit(left_arrow, (_LEFT + 570, _TOP + 319))
		screen.blit(right_arrow, (_LEFT + 630, _TOP + 319))
			
		if is_over_plot(self.close_button_plot):
			for i in range(3):
				screen.blit(get_image('misc/close_button'), self.close_button_plot[:2])