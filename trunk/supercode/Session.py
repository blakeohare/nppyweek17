import random

from supercode.Box import *
from supercode.Sprite import *

all_colors = 'red orange yellow lime green aqua blue purple pink brown'.split()
ALL_COLORS = all_colors # yeah, I'm too lazy to rename all instances of all_colors

polarities = 'h v n'.split()

STARTING_BUDGET = 1000
STARTING_ITEM_PRICE = 100

HEROES = 'superman batman'.split()
VILLAINS = 'joker riddler'.split()

class Session:
	def __init__(self):
		self.counter = 0
		self.balance = 0.5
		self.reputation = 1.0
		self.budget = STARTING_BUDGET
		self.spectrum_available = 1
		self.restocking = []
		self.prices = {}
		for color in all_colors:
			for polarity in polarities:
				key = polarity + '_' + color
				self.prices[key] = STARTING_ITEM_PRICE
		
	
	def item_sold(self, sprite, item):
		self.budget += self.prices[item]
	
	def pop_restocking(self):
		if len(self.restocking) > 0:
			t = self.restocking[0]
			self.restocking = self.restocking[1:]
			return t
		return None
	
	def order_more(self, color, free=False):
		# TODO: check to make sure you have enough funds
		
		if not free:
			self.budget -= 750
		
		for p in 'hvn':
			x = 4
			if p == 'n':
				x = 7
			for i in range(x):		
				self.restocking.append(p + '_' + color)
		random.shuffle(self.restocking)
	
	def get_last_available_color(self):
		t = int(self.budget // 1000)
		if t > self.spectrum_available and t < len(ALL_COLORS):
			self.spectrum_available += 1
		return ALL_COLORS[self.spectrum_available - 1]
	
	def get_random_box(self, is_free):
		# TODO: this function should weight itself on stuff
		color = random.choice(all_colors[:self.spectrum_available])
		polarity = random.choice(polarities)
		
		key = polarity + '_' + color
		
		if not is_free:
			price = self.prices[key]
			if self.budget >= price:
				self.budget -= self.prices[key]
			else:
				return None
		
		return Box(key)
	
	
	def update(self):
		self.counter += 1
	
	def check_for_customer(self):
		
		if self.counter % (3 * 5) == 0:
			pass
		else:
			return None
		
		is_hero = random.random() < .5
		
		list = HEROES if is_hero else VILLAINS
		
		key = random.choice(list)
		
		available_colors = ALL_COLORS[:self.spectrum_available]
		
		demands = []
		
		demand_count = int(random.random() * 3) + 1
		while demand_count > 0:
			color = random.choice(available_colors)
			neutral = random.random() < .5
			if not neutral:
				if is_hero:
					k = 'h_' + color
				else:
					k = 'v_' + color
			else:
				k = 'n_' + color
			demands.append(k)
			demand_count -= 1
		
		sprite = Sprite(key, is_hero, demands)
		
		return sprite
	
	def reject_last_customer(self):
		pass
		