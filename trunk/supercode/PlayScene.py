#import pygame # it'd be cool if I could leave this commented out

import random
from supercode.Util import *
from supercode.Sprite import *
from supercode.Box import *

_direction_to_vector = {
	'left': (-1, 0),
	'right': (1, 0),
	'up': (0, -1),
	'down': (0, 1)
}

_tile_info_lookup = {
	'c7': ('tiles/walltop-upperleft.png', False),
	'c8': ('tiles/walltop-uppermiddle.png', False),
	'c9': ('tiles/walltop-upperright.png', False),
	'c4': ('tiles/walltop-left.png', False),
	'c6': ('tiles/walltop-right.png', False),
	'c1': ('tiles/walltop-lowerleft.png', False),
	'c2': ('tiles/walltop-lowermiddle.png', False),
	'c3': ('tiles/walltop-lowerright.png', False),
	'c5': ('tiles/wall-bottom.png', False),
	'f1': ('tiles/floor-lowerleft.png', True),
	'f2': ('tiles/floor-lowermiddle.png', True),
	'f3': ('tiles/floor-lowerright.png', True),
	'f4': ('tiles/floor-left.png', True),
	'f5': ('tiles/floor-middle.png', True),
	'f6': ('tiles/floor-right.png', True),
	'f7': ('tiles/floor-upperleft.png', True),
	'f8': ('tiles/floor-uppermiddle.png', True),
	'f9': ('tiles/floor-upperright.png', True),

	'ct': ('tiles/counter-top.png', False),
	'cb': ('tiles/counter-bottom.png', False),
	
	'tl': ('tiles/counter-topleft.png', False),
	'bl': ('tiles/counter-bottomleft.png', False),
	
	'tr': ('tiles/counter-topright.png', False),
	'br': ('tiles/counter-bottomright.png', False),
	
	'C7': ('tiles/walltop-convex-lowerright.png', False),
	'C9': ('tiles/walltop-convex-lowerleft.png', False),
	'C1': ('tiles/walltop-convex-upperright.png', False),
	'C3': ('tiles/walltop-convex-upperleft.png', False),
	
	'F7': ('tiles/floor-convex-lowerright.png', True),
	'F9': ('tiles/floor-convex-lowerleft.png', True),
	'F1': ('tiles/floor-convex-upperright.png', True),
	'F3': ('tiles/floor-convex-upperleft.png', True),
	
	'xx': (None, True)
}

class Tile:
	def __init__(self, key):
		self.key = key
		self.stack = None
		data = _tile_info_lookup[key]
		self._passable = data[1]
		if data[0] == None:
			self.image = None
		else:
			self.image = get_image(data[0])
	
	def is_passable(self):
		return self._passable and (self.stack == None or len(self.stack) == 0)

class PlayScene:
	def __init__(self):
		self.next = self
		
		self.player = Sprite('player')
		self.player = Sprite('player')
		self.sprites = [self.player]
		
		self.sprites_by_row = None
		
		# Forgive me father for I am about to sin.
		m = [
			'c7 c8 c8 c8 c8 c8 c8 c8 c8 c8 c9 xx xx c7 c8 c8 c8 c8 c8 c8 c8 c9',
			'c4 c5 c5 c5 c5 c5 c5 c5 c5 c5 c6 xx xx c4 c5 c5 c5 c5 c5 c5 c5 c6',
			'c4 f7 f8 f8 f8 f8 f8 f8 f8 f9 c6 xx xx c4 f7 f8 f8 f8 f8 f8 f9 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 C1 c8 c8 C3 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c5 c5 c5 c5 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 F1 f8 f8 f8 f8 F3 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 F7 f2 f2 f2 f2 F9 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 C7 c2 c2 C9 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx xx c4 tl ct ct ct ct ct tr c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx xx c4 bl cb cb cb cb cb br c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx xx c4 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx xx c4 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx xx c4 f4 f5 f5 f5 f5 f5 f6 c6',
			'c4 f1 f2 f2 f2 f2 f2 f2 f2 f3 c6 xx xx c4 f1 f2 f2 f2 f2 f2 f3 c6',
			'c1 c2 c2 c2 c2 c2 c2 c2 c2 c2 c3 xx xx c1 c2 c2 c2 c2 c2 c2 c2 c3'
			]
		
		# Transpose this
		cols = []
		row_count = len(m)
		col_count = len(m[0].split())
		for i in range(len(m)):
			m[i] = m[i].split()
		x = 0
		while x < col_count:
			col = []
			y = 0
			while y < row_count:
				col.append(Tile(m[y][x]))
				y += 1
			x += 1
			cols.append(col)
			
		self.grid = cols
		
		self.player.x = 15.5
		self.player.y = 2.5
		
		self.set_up_boxes(10)
	
	def create_random_boxes(self, count):
		storage_left = 1
		storage_width = 5
		storage_top = 2
		storage_height = 5
		
		output = []
		colors = 'red yellow green blue aqua black white purple orange pink brown'.split()
		for i in range(count):
			box = Box(random.choice(colors), True)
			x = int(random.random() * storage_width) + storage_left
			y = int(random.random() * storage_height) + storage_top
			
			output.append([box, x, y])
			
		return output
		
	def set_up_boxes(self, count):
		boxes = self.create_random_boxes(count)
		for box in boxes:
			b = box[0]
			x = box[1]
			y = box[2]
			tile = self.grid[x][y]
			if tile.stack == None:
				tile.stack = []
			tile.stack.append(b)
	
	def lift(self, is_full):
		dxdy = _direction_to_vector[self.player.direction]
		x = int(self.player.x) + dxdy[0]
		y = int(self.player.y) + dxdy[1]
		tile = self.grid[x][y]
		
		if self.player.holding == None:
			if tile.stack != None:
				if is_full:
					self.player.holding = tile.stack
					tile.stack = None
				else:
					self.player.holding = [tile.stack[-1]]
					if len(tile.stack) == 1:
						tile.stack = None
					else:
						tile.stack = tile.stack[:-1]
		else:
			fix_loc = False
			if tile.stack == None:
				fix_loc = True
				tile.stack = []
			
			if is_full:
				tile.stack += self.player.holding
				self.player.holding = None
			else:
				a = self.player.holding[0]
				tile.stack.append(a)
				if len(self.player.holding) == 1:
					self.player.holding = None
				else:
					self.player.holding = self.player.holding[1:]
		
			# player could possibly set a box down and then be standing in an invalid position
			# nudge the player closer to the center of his tile to prevent this invalid state
			if fix_loc:
				if self.player.direction == 'left' or self.player.direction == 'right':
					left = self.player.direction == 'left'
					attempts = 10
					while self.player.is_overlapping(left) and attempts > 0:
						cx = int(self.player.x) + 0.5
						#cy = int(self.player.y) + 0.5 if (not horizontal) else self.player.y
						self.player.x = cx * .3 + self.player.x * .7
						#self.player.y = cy * .3 + self.player.y * .7
						attempts -= 1
					
					if attempts == 0: # my paranoia of some bug causing an infinite loop here
						self.player.x = int(self.player.x) + 0.5
						self.player.y = int(self.player.y) + 0.5
	
	def process_input(self, events, pressed_keys):
		for event in events:
			if event.down:
				if event.action == 'full' or event.action == 'single':
					self.lift(event.action == 'full')
		
		v = 1.3
		dx = 0
		dy = 0
		if pressed_keys.get('left'):
			dx = -1
		elif pressed_keys.get('right'):
			dx = 1
		if pressed_keys.get('up'):
			dy = -1
		elif pressed_keys.get('down'):
			dy = 1
		self.player.try_move(dx, dy)
			
	def update(self, counter):
		for sprite in self.sprites:
			sprite.update(self.grid, self.sprites)
	
	def render(self, screen, rcounter):
		screen.fill((0, 0, 0))
		self.render_room(screen, (50, 50), rcounter)

	def render_room(self, screen, roomtopleft, rcounter):
		rows = len(self.grid[0])
		cols = len(self.grid)
		grid = self.grid
		
		left = roomtopleft[0]
		top = roomtopleft[1]
		
		if self.sprites_by_row == None:
			i = 0
			self.sprites_by_row = []
			while i < rows:
				self.sprites_by_row.append([])
				i += 1
		
		i = 0
		while i < rows:
			self.sprites_by_row[i] = []
			i += 1
		
		for sprite in self.sprites:
			row = int(sprite.y)
			if row >= 0 and row < rows:
				self.sprites_by_row[row].append(sprite)
		
		row = 0
		while row < rows:
			col = 0
			while col < cols:
				tile = self.grid[col][row]
				img = tile.image
				if img != None:
					screen.blit(img, (col * 16 + left, row * 16 + top))
					if tile.stack != None:
						i = 0
						x = col + 0.5
						y = row + 0.5
						for box in tile.stack:
							box.render(screen, left, top, x, y, i)
							i += 1
				col += 1
			
			for sprite in self.sprites_by_row[row]:
				sprite.render(screen, left, top, rcounter)
				if sprite.holding != None:
					i = 4
					for box in sprite.holding:
						box.render(screen, left, top, sprite.x, sprite.y, i)
						i += 1
			row += 1
		
		