import pygame
import os

from supercode.Util import *

_config = {'t': 'arrows'}

if os.path.exists('config.txt'):
	c = open('config.txt', 'rt')
	t = trim(c.read().lower())
	c.close()

	if t in ('arrows', 'qwerty', 'dvorak'):
		_config['t'] = t

def save_input():
	v = _config['t']
	c = open('config.txt', 'wt')
	c.write(v)
	c.close()


class InputConfigMenu:
	def __init__(self):
		self.next = self
		self.bg = get_image('misc/input_config').convert()
		self.check = get_image('misc/check')
		self.plots = [
			(298, 352, 261, 50, 'qwerty'),
			(575, 352, 158, 50, 'dvorak'),
			(775, 352, 176, 50, 'arrows'),
			(900, 0, 100, 100, 'exit')
		]
	def update(self, counter):
		pass
	
	def get_plot(self):
		mx = mouse_x()
		my = mouse_y()
		for plot in self.plots:
			if plot[0] < mx:
				if plot[1] < my:
					if plot[0] + plot[2] > mx:
						if plot[1] + plot[3] > my:
							return plot[4]
		return None
	
	def process_input(self, events, pressed):
		plot = self.get_plot()
		for event in events:
			if event.down:
				if event.action == 'lclick':
					if plot != None:
						if plot == 'exit':
							from supercode.TitleScene import TitleScene
							self.next = TitleScene()
						else:
							_config['t'] = plot
							save_input()
							play_sound('click')
							break
			
	
	def render1(self, screen, counter):
		pass
	
	def render2(self, screen, counter):
		screen.blit(self.bg, (0, 0))
		
		plot = self.get_plot()
		exit_count = 1
		box = None
		if plot == 'exit':
			exit_count = 5
		elif plot != None:
			for p in self.plots:
				if plot == p[4]:
					box = p
					break
		
		for i in range(exit_count):
			screen.blit(get_image('misc/close_button'), (940, 10))
		
		for p in self.plots:
			if p[4] != 'exit':
				if p[4] == _config['t']:
					screen.blit(get_image('misc/check'), (p[0] + p[2] - 35, p[1] - 52))
		
		if box != None:
			pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(box[0], box[1], box[2], box[3]), 3)