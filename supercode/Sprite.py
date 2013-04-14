import os
from supercode.Util import *

_max_walk_lookup = {}

class Sprite:
	def __init__(self, key):
		self.max_walk = self.get_max_walk(key)
		self.key = key
		self.x = 0.0
		self.y = 0.0
		self.dx = 0.0
		self.dy = 0.0
		self.v = 3.3 # TODO: adjust per sprite type
		self.walking = False
		self.direction = 'down'
	
	def get_max_walk(self, key):
		if len(_max_walk_lookup) == 0:
			path = 'images/sprites/max_walk.txt'
			path = path.replace('/', os.sep)
			c = open(path, 'rt')
			lines = c.read().split('\n')
			c.close()
			for line in lines:
				line = trim(line)
				if len(line) > 0:
					parts = line.split(':')
					_max_walk_lookup[trim(parts[0])] = int(trim(parts[1]))
		return _max_walk_lookup[key]
	
	def try_move(self, dx, dy):
		if dx == 0 and dy == 0:
			self.walking = False
			self.dx = 0.0
			self.dy = 0.0
		else:
			self.walking = True
			self.dx = self.v * dx
			self.dy = self.v * dy
			if dx < 0: self.direction = 'left'
			elif dx > 0: self.direction = 'right'
			if dy < 0: self.direction = 'up'
			elif dy > 0: self.direction = 'down'
	
	def update(self, grid, others):
		dx = self.dx / 16.0
		dy = self.dy / 16.0
		
		old_col = int(self.x)
		old_row = int(self.y)
		new_col = int(self.x + dx)
		new_row = int(self.y + dy)
		
		left_col = int(self.x + dx - 6.0 / 16.0)
		right_col = int(self.x + dx + 6.0 / 16.0)
		
		passes = True
		for col_check in (left_col, new_col, right_col):
			tile = grid[col_check][new_row]
			if not tile.is_passable():
				passes = False
				break
		
		if passes:
			self.x += dx
			self.y += dy
		
		self.dx = 0.0
		self.dy = 0.0
	
	def render(self, screen, offsetx, offsety, counter):
		if self.walking:
			file = ''.join([
				'sprites/',
				self.key,
				'_walking_',
				self.direction,
				'_',
				str((counter // 2) % self.max_walk + 1),
				'.png'])
		else:
			file = ''.join([
				'sprites/',
				self.key,
				'_standing_',
				self.direction,
				'.png'])
		img = get_image(file)
		x = offsetx + int(self.x * 16 - 8)
		y = offsety + int(self.y * 16 - 32)
		screen.blit(get_image(file), (x, y))