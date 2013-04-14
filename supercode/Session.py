import random

from supercode.Box import *
from supercode.Sprite import *

all_colors = 'blue red orange yellow lime green aqua purple pink brown'.split()
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
		self.spectrum_available = 2
		
		self.prices = {}
		for color in all_colors:
			for polarity in polarities:
				key = polarity + '_' + color
				self.prices[key] = STARTING_ITEM_PRICE
		
	
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
		
		sprite = Sprite(key, is_hero, ['n_blue'])
		
		return sprite
	
	def reject_last_customer(self):
		pass
		