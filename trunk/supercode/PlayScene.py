#import pygame # it'd be cool if I could leave this commented out

import random

from supercode.Box import *
from supercode.NewProductsMenu import *
from supercode.OrderStuffMenu import *
from supercode.PriceMenu import *
from supercode.Session import *
from supercode.Sprite import *
from supercode.Util import *

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
		self.passable = data[1]
		self.is_counter = False
		if data[0] == None:
			self.image = None
		else:
			self.image = get_image(data[0])
	
	def is_passable(self):
		return self.passable and (self.stack == None or len(self.stack) == 0)

class PlayScene:
	def __init__(self):
		self.next = self
		
		self.session = Session()
		self.player = Sprite('player')
		self.player = Sprite('player')
		self.sprites = [self.player]
		self.last_color = None
		self.sprites_by_row = None
		
		# Forgive me father for I am about to sin.
		m = [
			'xx xx xx xx xx xx xx xx c7 c8 c8 c8 c8 c8 c8 c8 c8 c8 c9 xx xx xx xx xx xx xx xx',
			'c7 c8 c8 c8 c8 c8 c9 xx c4 c5 c5 c5 c5 c5 c5 c5 c5 c5 c6 xx c7 c8 c8 c8 c8 c8 c9',
			'c4 c5 c5 c5 c5 c5 c6 xx c4 f7 f8 f8 f8 f8 f8 f8 f8 f9 c6 xx c4 c5 c5 c5 c5 c5 c6',
			'c4 f7 f8 f8 f8 f9 C1 c8 C3 f4 f5 f5 f5 f5 f5 f5 f5 f6 C1 c8 C3 f7 f8 f8 f8 f9 c6',
			'c4 f4 f5 f5 f5 f6 c5 c5 c5 f4 f5 f5 f5 f5 f5 f5 f5 f6 c5 c5 c5 f4 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 F1 f8 f8 f8 F3 f5 f5 f5 f5 f5 f5 f5 F1 f8 f8 f8 F3 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 F7 f2 f2 f2 F9 f5 f5 f5 f5 f5 f5 f5 F7 f2 f2 f2 F9 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f6 C7 c2 C9 f4 f5 f5 f5 f5 f5 f5 f5 f6 C7 c2 C9 f4 f5 f5 f5 f6 c6',
			'c4 tl ct ct ct tr c6 xx c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx c4 tl ct ct ct tr c6',
			'c4 bl cb cb cb br c6 xx c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx c4 bl cb cb cb br c6',
			'c4 f4 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f6 c6',
			'c4 f4 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f5 f5 f5 f5 f6 c6 xx c4 f4 f5 f5 f5 f6 c6',
			'c4 f1 f2 f5 f2 f3 c6 xx c4 f1 f2 f2 f2 f2 f2 f2 f2 f3 c6 xx c4 f1 f2 f5 f2 f3 c6',
			'c1 c2 c2 f5 c2 c2 c3 xx c1 c2 c2 c2 c2 c2 c2 c2 c2 c2 c3 xx c1 c2 c2 f5 c2 c2 c3'
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
		
		for i in range(5):
			v = self.grid[1 + i][8]
			h = self.grid[21 + i][8]
			v.is_counter = True
			h.is_counter = True
			v.counter_slot = i
			h.counter_slot = i
			v.counter_is_hero = False
			h.counter_is_hero = True
		
		self.player.x = 14.5
		self.player.y = 12.5
		
		#self.set_up_boxes(10)
		self.session.order_more('red', True)

	def place_box(self, key):
		storage_left = 11
		storage_width = 5
		storage_top = 2
		storage_height = 5
		
		box = Box(key)
		while True:
			x = storage_left + int(random.random() * storage_width)
			y = storage_top + int(random.random() * storage_height)
			dx = abs(x - self.player.x)
			dy = abs(y - self.player.y)
			if dx > 2 or dy > 2:
				break
		
		tile = self.grid[x][y]
		if tile.stack == None:
			tile.stack = []
		tile.stack.append(box)
	
	def create_random_boxes(self, count):
		storage_left = 11
		storage_width = 5
		storage_top = 2
		storage_height = 5
		
		output = []
		
		for i in range(count):
			box = self.session.get_random_box(True)
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
	
	def incorrect_order(self):
		play_sound("incorrect_order")
		pass
	
	def lift(self, is_full):
		dxdy = _direction_to_vector[self.player.direction]
		x = int(self.player.x) + dxdy[0]
		y = int(self.player.y) + dxdy[1]
		tile = self.grid[x][y]
		
		if self.player.holding == None:
			if tile.stack != None and not tile.is_counter:
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
			if not tile.passable and not tile.is_counter:
				play_sound('cant_drop_box')
				return
			
			to_drop = []
			
			if is_full:
				to_drop = self.player.holding[:]
			else:
				to_drop = self.player.holding[:1]
			
			item_sold = False
			
			if tile.is_counter:
				for sprite in self.sprites:
					if sprite.phase == 4:
						if sprite.counter_slot == tile.counter_slot:
							if sprite.is_hero == tile.counter_is_hero:
								sprite_demands = sprite.demands[:]
								for item_to_drop in to_drop:
									found = False
									i = 0
									while i < len(sprite_demands):
										d = sprite_demands[i]
										if d == item_to_drop.key:
											found = True
											sprite_demands = sprite_demands[:i] + sprite_demands[i + 1:]
											break
										i += 1
									if not found:
										self.incorrect_order()
										return
								self.session.item_sold(sprite, item_to_drop.key)
								item_sold = True
								break
			
			if item_sold:
				play_sound('money_sound')
			elif tile.is_counter:
				# can't drop a box on a counter without selling it
				return
			
			if tile.stack == None:
				fix_loc = True
				tile.stack = []
			
			if is_full:
				for item in self.player.holding:
					tile.stack.append(item)
				self.player.holding = None
			else:
				tile.stack.append(self.player.holding[0])
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
				elif event.action == 'menu':
					self.next = PriceMenu(self)
				elif event.action == 'order':
					self.next = OrderStuffMenu(self)
		
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
		self.session.update()
		if counter % 10 == 0:
			r = self.session.pop_restocking()
			if r != None:
				self.place_box(r)
				
		c = self.session.get_last_available_color()
		if c != self.last_color:
			self.last_color = c
			self.next = NewProductsMenu(self, c)
		customers = self.session.check_for_customers()
		
		if customers != None:
			for customer in customers:
				is_hero = customer.is_hero
				taken = {}
				for i in range(5):
					taken[i] = False
				for sprite in self.sprites:
					if sprite != self.player and sprite.is_hero == is_hero:
						taken[sprite.counter_slot] = True
				open = []
				for k in taken.keys():
					if not taken[k]:
						open.append(k)
				random.shuffle(open)
				
				if (len(open) > 0):
					customer.set_counter_slot(open[0])
					self.sprites.append(customer)
				else:
					# counter full. reject customer
					self.session.reject_last_customer()
		
		for sprite in self.sprites:
			if sprite != self.player:
				sprite.automate(self.grid)
		
		new_sprites = []
		for sprite in self.sprites:
			if not sprite.destroy_me:
				sprite.update(self.grid, self.sprites)
				new_sprites.append(sprite)
		self.sprites = new_sprites
	
	def render2(self, screen, counter):
		x_coords = [
			0,
			75,
			149,
			201,
			243
		]
		t = 30
		icon_x = [
			x_coords[0] + t + 6,
			x_coords[1] + t + 6,
			x_coords[2] + t + 6,
			x_coords[3] + t + 28,
			x_coords[4] + t + 52
		]
		hero_offset = 621
		spacing = 40
		for sprite in self.sprites:
			if sprite != self.player:
				if sprite.phase == 4:
					slot = sprite.counter_slot
					demand_x = 8 + x_coords[slot]
					offset = 0
					if sprite.is_hero:
						offset = hero_offset
					demand_x += offset
					
					
					img = get_image('misc/demand_' + str(sprite.counter_slot + 1))
					screen.blit(img, (demand_x, screen.get_height() - img.get_height() - 20))
					height = len(sprite.demands) * spacing
					icon_y = 620 - height // 2
					for d in sprite.demands:
						screen.blit(get_image('boxes/' + d), (icon_x[slot] + offset, icon_y))
						icon_y += spacing
		
		self.draw_budget_bar(screen)
		self.draw_power_balance(screen)
		self.draw_options(screen)
		
		screen.blit(get_image('misc/radio'), (529, 615))
	
	def draw_options(self, screen):
		
		prices = get_small_text("Adjust prices (R)")
		order_more = get_small_text("Restock (T)")
		cloud = get_image('misc/thought_cloud')
		x = screen.get_width() - cloud.get_width() - 20
		y = 0
		screen.blit(cloud, (x, y))
		screen.blit(prices, (x + 73, y + 40))
		screen.blit(order_more, (x + 73, y + 70))
		
	
	def draw_power_balance(self, screen):
		left = 416
		top = 564
		text = get_small_text("Power Balance")
		screen.blit(text, (left, top))
		
		width = 220
		y = top + text.get_height() + 10
		x = left + text.get_width() // 2 - width // 2
		
		evil = int(self.session.balance * width)
		good = width - evil
		height = 20
		border = 3
		pygame.draw.rect(screen, (123, 123, 123), pygame.Rect(x - border, y - border, width + border * 2, height + border * 2))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, evil, height))
		x += evil
		pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, good, height))
		
	
	def draw_budget_bar(self, screen):
		screen.blit(get_image('misc/budget_bar'), (10, 10))
		screen.blit(get_text("Budget: " + format_money(self.session.budget)), (30, 38))
		
				
					
	def render1(self, screen, rcounter):
		screen.fill((100, 180, 255))
		self.render_room(screen, (27, 45), rcounter)

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
					i = 4.7
					for box in sprite.holding:
						box.render(screen, left, top, sprite.x, sprite.y, i)
						i += 1
			row += 1
		
		