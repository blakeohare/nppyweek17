import pygame

class TitleScene:
	def __init__(self):
		self.next = self
	
	def process_input(self, events):
		for event in events:
			if event.action == 'lift':
				self.next = None
	
	def update(self, counter):
		pass
	
	def render(self, screen, render_counter):
		screen.fill((255, 255, 0))