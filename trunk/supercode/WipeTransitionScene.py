# I'll finish this later. Just tired of seeing this on the submit menu

import pygame 

class WipeTransitionScene:
	def __init__(self, from_scene, to_scene):
		self.next = self
		self.from_scene = from_scene
		self.to_scene
		self.counter = 0
		self.phase = 0
		self.per_phase = 30
	
	def process_input(self, events):
		pass
	
	def update(self, counter):
		self.counter += 1
		progress = 1.0 * self.counter / self.per_phase
		if progress >= 1.0:
			progress -= 1
			self.phase += 1
		self.progress = progress