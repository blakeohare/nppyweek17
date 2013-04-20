from supercode.JukeBox import *
from supercode.Util import *

MAX_FADE = 18

class IntroSlideshow:
	def __init__(self):
		self.next = self
		self.current = 0
		self.target = None
		self.fade = 0
		self.black = {}
		
		self.images = [
			get_image('intro/slide1'),
			get_image('intro/slide2'),
			get_image('intro/slide3'),
			get_image('intro/slide4'),
			get_image('intro/slide5'),
			get_image('intro/slide6'),
			get_image('intro/slide7'),
			get_image('intro/slide8'),
			get_image('intro/slide9'),
			get_image('intro/slide10'),
			get_image('intro/slide11'),
			get_image('intro/slide12'),
			get_image('intro/slide13')
		]
		
		self.images = legacy_map(lambda x:x.convert(), self.images)
		
	
	def update(self, counter):
		ensure_playing('tutorial')
		if self.target != None:
			self.fade += 1
		
		if self.fade >= MAX_FADE:
			self.fade = 0
			self.current = self.target
			self.target = None
			
		if self.current == len(self.images):
			from supercode.TitleScene import TitleScene
			self.next = TitleScene()
	
	def process_input(self, events, pressed):
		if self.target == None:
			c = self.current
			n = None
			for event in events:
				if event.down and n == None:
					if event.action == 'left':
						n = c - 1
					elif event.action == 'right':
						n = c + 1
					elif event.action == 'pause':
						n = c + 1
			self.target = n
			
	def get_black(self, opacity, screen):
		img = self.black.get(opacity, None)
		if img == None:
			black = screen.copy()
			black.fill((0, 0, 0))
			black.set_alpha(opacity)
			self.black[opacity] = black
			img = black
		return img
	
		
	def render1(self, screen, rcounter):
		pass
	
	def render2(self, screen, rcounter):
		prev_img = None
		next_img = None
		if self.current < len(self.images):
			prev_img = self.images[self.current]
		if self.target != None and self.target < len(self.images):
			next_img = self.images[self.target]
		
		
		if self.target == None:
			img = prev_img
			opacity = 255
		else:
			progress = 1.0 * self.fade / MAX_FADE
			aprogress = 1.0 - progress
			if progress < 0.5:
				img = prev_img
				opacity = 255 - int(progress * 2 * 255)
			else:
				img = next_img
				opacity = int((progress - .5) * 2 * 255)
		
		if img == None:
			screen.fill((0, 0, 0))
		else:
			if opacity < 0: opacity = 0
			if opacity > 255: opacity = 255
			
			screen.blit(img, (0, 0))
			if opacity != 255:
				b = self.get_black(255 - opacity, screen)
				screen.blit(b, (0, 0))
			