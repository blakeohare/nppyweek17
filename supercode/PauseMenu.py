import pygame

from supercode.TitleScene import *
from supercode.Util import *

class PauseMenu:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.img = None
		self.index = 0
	
	def update(self, counter):
		pass
	
	def process_input(self, events, pressed_keys):
		for event in events:
			if event.down:
				if event.action == 'up':
					if self.index > 0:
						self.index -= 1
				elif event.action == 'down':
					if self.index < 3:
						self.index += 1
				elif event.action == 'pause':
					self.do(self.index)
	
	def do(self, index):
		if index == 0: # resume
			self.bg.next = self.bg
			self.next = self.bg
		elif index == 1: # make funny noise
			pass # TODO: this
		elif index == 2: # exit to menu
			from supercode.TitleScene import TitleScene # dafuq? why will the next line not work even though this is at the top of the file?
			self.next = TitleScene()
		elif index == 3: # exit the game
			self.next = None # TODO: simple exit screen like Katamari Damacy?
	
	def render1(self, screen, rcounter):
		pass
	
	def render2(self, screen, rcounter):
		if self.img == None:
			s1 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
			self.bg.render1(s1, rcounter)
			self.img = pygame.Surface(screen.get_size())
			pygame.transform.scale(s1, screen.get_size(), self.img)
			self.bg.render2(self.img, rcounter)
			dark = pygame.Surface(screen.get_size()).convert()
			dark.fill((0, 0, 0,))
			dark.set_alpha(180)
			self.img.blit(dark, (0, 0))
			menu = get_image('misc/price_menu_bg')
			x = (screen.get_width() - menu.get_width()) // 2
			y = (screen.get_height() - menu.get_height()) // 2
			self.img.blit(menu, (x, y))
			text = get_text("Paused!")
			x += 30
			y += 30
			self.img.blit(text, (x, y))
			
			options = ["Resume", "Make funny noise", "Quit to Menu", "Exit to DOS"]
			x += 90
			y += text.get_height() + 55
			
			self.option_loc = []
			for option in options:
				self.option_loc.append((x, y))
				txt = get_text(option)
				self.img.blit(txt, (x + 30, y))
				y += txt.get_height() + 20
			
		screen.blit(self.img, (0, 0))
		
		cursor = self.option_loc[self.index]
		screen.blit(get_arrow('right', True, rcounter // 3), (cursor[0] - 15, cursor[1] - 10))