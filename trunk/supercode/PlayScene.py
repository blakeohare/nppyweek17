#import pygame # it'd be cool if I could leave this commented out

from supercode.Util import *
from supercode.Sprite import *

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
		self.passable = data[1]
		if data[0] == None:
			self.image = None
		else:
			self.image = get_image(data[0])

class PlayScene:
	def __init__(self):
		self.next = self
		
		self.player = Sprite('player')
		self.player = Sprite('player')
		self.sprites = [self.player]
		
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
		
		self.player.x = 1.5
		self.player.y = 2.5
		
	def process_input(self, events, pressed_keys):
		for event in events:
			pass
		
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
		
		row = 0
		while row < rows:
			col = 0
			while col < cols:
				img = self.grid[col][row].image
				if img != None:
					screen.blit(img, (col * 16 + left, row * 16 + top))
				col += 1
			row += 1
		
		self.render_sprites(screen, roomtopleft, rcounter)
		
	def render_sprites(self, screen, roomtopleft, rcounter):
		top = roomtopleft[1]
		left = roomtopleft[0]
		for sprite in self.sprites:
			sprite.render(screen, left, top, rcounter)