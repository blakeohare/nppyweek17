from supercode.Util import *

class Box:
	def __init__(self, color, is_good):
		self.color = color
		self.is_good = is_good
		self.img = get_image('boxes/box_' + color)
	
	def render(self, screen, left, top, game_x, game_y, height):
		x = int(left + game_x * 16 - 8)
		y = int(top + game_y * 16 - 16 - height * 8)
		screen.blit(self.img, (x, y))