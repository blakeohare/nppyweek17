import os
from supercode.Util import *

_max_walk_lookup = {}
_collide_margin = 6.0 / 16.0

HERO_DOOR = (23, 14)
HERO_COUNTER_LEFT = (HERO_DOOR[0] - 1, HERO_DOOR[1] - 4)

VILLAIN_DOOR = (3, 14)
VILLAIN_COUNTER_LEFT = (VILLAIN_DOOR[0] - 1, VILLAIN_DOOR[1] - 4)

SIDEWAYS_Y = HERO_DOOR[1] - 1.5

class Sprite:
	def __init__(self, key, is_hero=False, demands=[], target=None):
		self.max_walk = self.get_max_walk(key)
		self.is_hero = is_hero
		self.demands = demands
		self.key = key
		self.x = 0.0
		self.y = 0.0
		self.dx = 0.0
		self.dy = 0.0
		self.v = 3.3 # TODO: adjust per sprite type
		self.walking = False
		self.direction = 'down'
		self.holding = None
		self.phase = 0
		self.counter_slot = -1
		self.lifetime = 0
		self.destroy_me = False
	
	def set_counter_slot(self, n):
		self.counter_slot = n
	
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
	
	def is_overlapping(self, left):
		x = int(self.x)
		m = _collide_margin
		if left:
			m *= -1
		x0 = int(self.x + m)
		if x == x0:
			return False
		return True
	
	
	# Phases:
	# 1 - walk through door and up
	# 2 - Walk sideways to target X
	# 3 - Walk up to counter
	# 4 - Wait at counter
	# 5 - Walk down to back wall
	# 6 - walk sideways to door X
	# 7 - Walk down out of door
	def automate(self, grid):
		
		door = HERO_DOOR if self.is_hero else VILLAIN_DOOR
		door = (door[0] + .5, door[1])
		counter_left = HERO_COUNTER_LEFT if self.is_hero else VILLAIN_COUNTER_LEFT
		counter_y = counter_left[1]
		counter_x = counter_left[0]
		
		# put them in the doorway
		if self.phase == 0:
			self.x, self.y = door
			self.phase = 1
		
		# walk through door and up until you hit SIDEWAYS_Y
		if self.phase == 1:
			if self.y < SIDEWAYS_Y:
				self.phase = 2
				self._p_origin = self.x
			else:
				self.dy = -1
				return
		
		# walk sideways to your self.counter_slot
		if self.phase == 2:
			target = counter_x + (self.counter_slot - 1) + .5
			if self._p_origin == target:
				self.phase = 3
			elif self._p_origin < target: # walk right
				if self.x >= target:
					self.phase = 3
				else:
					self.dx = 1
					return
			elif self._p_origin > target: # walk left
				if self.x <= target:
					self.phase = 3
				else:
					self.dx = -1
					return
		
		# walk up to the counter
		if self.phase == 3:
			go_to_y = counter_y + 1.5 # middle of the tile in front of the counter
			if self.y <= go_to_y:
				self.phase = 4
			else:
				self.dy = -1
				return
		
		# wait until you have your order
		if self.phase == 4:
			
			cx = int(self.x)
			cy = int(counter_y - 2)
			tile = grid[cx][cy]
			
			if tile.stack != None:
				for item in tile.stack:
					if not item.accounted and item.key in self.demands:
						i = 0
						while i < len(self.demands):
							if self.demands[i] == item.key:
								self.demands = self.demands[:i] + self.demands[i + 1:]
								item.accounted = True
								break
							i += 1
							
			
			if len(self.demands) == 0:
				self.phase = 5
				self.holding = tile.stack
				tile.stack = None
			else:
				return 
		
		# walk down until you hit sideways_y
		if self.phase == 5:
			if self.y < SIDEWAYS_Y:
				self.dy = 1
				return
			else:
				self.phase = 6
				self._p_origin = self.x
		
		# walk horizontally until you hit the door x
		if self.phase == 6:
			target = door[0]
			if self._p_origin == target:
				self.phase = 7
			elif self._p_origin < target: # walk right to door point
				if self.x >= door[0]:
					self.phase = 7
				else:
					self.dx = 1
					return
			elif self._p_origin > target: # walk left to door point
				if self.x <= door[0]:
					self.phase = 7
				else:
					self.dx = -1
					return
		
		# walk down until you hit the door, then kill yourself
		if self.phase == 7:
			if self.y < door[1]:
				self.dy = 1
				return
			else:
				self.destroy_me = True
		
			
		
	def update(self, grid, others):
		dx = self.dx / 16.0
		dy = self.dy / 16.0
		
		old_col = int(self.x)
		old_row = int(self.y)
		new_col = int(self.x + dx)
		new_row = int(self.y + dy)
		
		left_col = int(self.x + dx - _collide_margin)
		right_col = int(self.x + dx + _collide_margin)
		
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
		self.lifetime += 1
		
	
	
	def render(self, screen, offsetx, offsety, counter):
		hold = 'hold_' if self.holding else ''
		
		#TODO: remove this when the other characters are checked in with hold images
		if self.key != 'player':
			hold = ''
		
		
		if self.walking:
			file = ''.join([
				'sprites/',
				self.key,
				'_',
				hold,
				'walking_',
				self.direction,
				'_',
				str((counter // 4) % self.max_walk + 1),
				'.png'])
		else:
			file = ''.join([
				'sprites/',
				self.key,
				'_',
				hold,
				'standing_',
				self.direction,
				'.png'])
		img = get_image(file)
		x = offsetx + int(self.x * 16 - 8)
		y = offsety + int(self.y * 16 - 32)
		screen.blit(get_image(file), (x, y))