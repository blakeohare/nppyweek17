import random

from supercode.Box import *
from supercode.Sprite import *
from supercode.Tweaks import *

class Session:
	def __init__(self):
		self.counter = 0
		self.balance = 0.5
		self.reputation = 1.0
		self.budget = STARTING_BUDGET
		self.spectrum_available = 1
		self.restocking = []
		self.prices = {}
		for color in ALL_COLORS:
			for polarity in POLARITIES:
				key = polarity + '_' + color
				self.prices[key] = STARTING_ITEM_PRICE
		
	
	def item_sold(self, sprite, item):
		self.budget += self.prices[item]
		if sprite.is_hero:
			self.balance -= BALANCE_SALE_OFFSET
		else:
			self.balance += BALANCE_SALE_OFFSET
	
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
		color = random.choice(ALL_COLORS[:self.spectrum_available])
		polarity = random.choice(POLARITIES)
		
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
		b = self.balance
		b = (b * 2 - 1) * BALANCE_MULTIPLIER
		b = (b + 1) / 2.0
		self.balance = b
	
	def check_for_customers(self):
		# Do the calculation individually for heros and villains.
		# Return a list of 1, or 2 customers or None
		output = None
		for ih in (True, False):
			customer = self.check_for_customer_by_polarity(ih)
			if customer != None:
				if output == None:
					output = []
				output.append(customer)
		return output
	
	def check_for_customer_by_polarity(self, is_hero):
		
		# Customer presence is determined in two phases. First
		# the average price for that customer type is computed.
		# The average price allure is then computed.
		
		# 1 customer appears every 20 seconds on average.
		# At 30 fps, this is 1 / 600, when all prices are $100.
		
		# The allure ratio is multiplied to the denominator and creates
		# a value X.
		
		# If random.random() is less than X, a customer is created.
		
		x = 1.0 / (NORMAL_CUSTOMER_FREQUENCY * 30)
		p = ('h', 'n') if is_hero else ('v', 'n') # polarities relevant
		colors = ALL_COLORS[:self.spectrum_available]
		total_price = 0
		average_price = 0
		for color in colors:
			for polarity in p:
				average_price += 100
				total_price += self.prices[polarity + '_' + color]
		
		allure = 1.0 * average_price / total_price
		
		x *= allure
		
		if random.random() > x:
			return None
		
		character_key = random.choice(HEROES if is_hero else VILLAINS)
		
		# 2 colors or less: 1 demand
		# 5 colors or less: 1 or 2 demands
		# 8 colors or less: 1 to 3 demands
		# 9 or more colors: 2 to 4 demands
		lc = len(colors)
		if lc < 3:
			num_demands = [1]
		elif lc < 6:
			num_demands = [1, 2]
		elif lc < 9:
			num_demands = [1, 2, 3]
		else:
			num_demands = [2, 3, 4]
		num_demands = random.choice(num_demands)
		
		demands = self.get_demands(num_demands, is_hero)
		
		sprite = Sprite(character_key, is_hero, demands)
		
		return sprite
	
	def get_price_table(self, is_hero):
		output = []
		for color in ALL_COLORS[:self.spectrum_available]:
			for p in ('hn' if is_hero else 'vn'):
				k = p + '_' + color
				allure = 100.0 / self.prices[k]
				if len(output) == 0:
					output.append((k, allure))
				else:
					output.append((k, output[-1][1] + allure))
		return output
	
	def get_demands(self, num, is_hero):
		ptable = self.get_price_table(is_hero)
		max_p = ptable[-1][1]
		output = []
		for i in range(num):
			x = random.random() * max_p
			for t in ptable:
				if x <= t[1]:
					output.append(t[0])
					break
		if len(output) == 0: # this should never happen...but just in case...
			return ['n_red']
		return output
	
	def reject_last_customer(self):
		pass
		