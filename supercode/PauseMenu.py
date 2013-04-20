import pygame

class PauseMenu:
	def __init__(self, bg):
		self.next = self
		self.bg = bg
		self.img = None
	
	def update(self, counter):
		pass
	
	def process_input(self, events, pressed_keys):
		pass
	
	def render1(self, screen, rcounter):
		pass
	
	def render2(self, screen, rcounter):
		if self.img == None:
			s1 = pygame.Surface((screen.get_width() // 2, screen.get_height() // 2))
			self.bg.render1(s1, rcounter)
			self.img = pygame.Surface(screen.get_size())
			pygame.transform.scale(s1, screen.get_size(), self.img)
			self.bg.render2(self.img, rcounter)
		screen.blit(self.img, (0, 0))
		
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(80, 80, screen.get_width() - 80 * 2, screen.get_height() - 80 * 2))
