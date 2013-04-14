import random

from supercode.Box import *

all_colors = 'red orange yellow lime green aqua blue purple pink brown'.split()
polarities = 'h v n'.split()

STARTING_BUDGET = 1000
STARTING_ITEM_PRICE = 100

class Session:
	def __init__(self):
		self.balance = 0.5
		self.reputation = 1.0
		self.budget = STARTING_BUDGET
		
		self.prices = {}
		for color in all_colors:
			for polarity in polarities:
				key = polarity + '_' + color
				self.prices[key] = STARTING_ITEM_PRICE
		
	
	def get_random_box(self, is_free):
		# TODO: this function should weight itself on stuff
		color = random.choice(all_colors)
		polarity = random.choice(polarities)
		
		key = polarity + '_' + color
		
		if not is_free:
			price = self.prices[key]
			if self.budget >= price:
				self.budget -= self.prices[key]
			else:
				return None
		
		return Box(key)
	