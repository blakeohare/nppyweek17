from supercode.JukeBox import *
from supercode.Util import *

_c = 0
def nextC():
	global _c
	x = _c
	_c += 1
	return x

PHASE_FADE_IN = nextC()
PHASE_POST_FADE = nextC()
PHASE_SHOW_LABELS = nextC()
PHASE_TICK_UP = nextC()
PHASE_SPIN = nextC()
PHASE_FADE_OUT = nextC()

class DefeatScene:
	def __init__(self, heroes_win, time, money):
		self.heros = heroes_win
		self.bg = get_image('intro/' + ('hero_win' if self.heros else 'villain_win')).convert()
		self.next = self
		self.counter = 0
		self.phase = 0
		self.time = time
		self.money = money
		self.score = time + money
		self.max_counter = {
			PHASE_FADE_IN : 30,
			PHASE_POST_FADE : 90,
			PHASE_SHOW_LABELS : 15,
			PHASE_TICK_UP : 30,
			PHASE_SPIN : -1,
			PHASE_FADE_OUT : 60,
		}
		self.black = None
	
	def update(self, counter):
		ensure_playing(None)
		self.counter += 1
		if self.phase != PHASE_SPIN and self.counter >= self.max_counter[self.phase]:
			self.counter = 0
			self.phase += 1
			if self.phase >= len(self.max_counter):
				self.phase = PHASE_FADE_OUT
				from supercode.TitleScene import TitleScene
				self.next = TitleScene()
	
	def process_input(self, events, pressed):
		if self.phase == PHASE_SPIN:
			for event in events:
				if event.down and event.action in ('pause', 'lclick', 'rclick'):
					self.phase += 1
					break
	
	def render1(self, screen, rcounter):
		pass
	
	def render2(self, screen, rcounter):
		screen.blit(self.bg, (0, 0))
		progress = 1.0 * self.counter / self.max_counter[self.phase]
		if progress < 0.0: progress = 0.0
		if progress > 1.0: progress = 1.0
		
		if self.black == None:
			self.black = screen.copy().convert()
			self.black.fill((0, 0, 0))
		
		if self.phase == PHASE_FADE_IN:
			self.black.set_alpha(int(255 * (1 - progress)))
			screen.blit(self.black, (0, 0))
		elif self.phase == PHASE_POST_FADE:
			pass
		else:
			
			ty = 180
			my = 320
			sy = 460
			if self.phase >= PHASE_SHOW_LABELS:
				screen.blit(get_text("Time:"), (659, ty))
				screen.blit(get_text("Money:"), (659, my))
				screen.blit(get_text("Score:"), (659, sy))
			
			time_shown = self.time
			money_shown = self.money
			score_shown = self.score
			
			if self.phase == PHASE_TICK_UP:
				time_shown = int(self.time * progress)
				money_shown = int(self.money * progress)
				score_shown = int(self.score * progress)
			
			if self.phase >= PHASE_TICK_UP:
				screen.blit(get_text(str(time_shown)), (690, ty + 30))
				screen.blit(get_text(str(money_shown)), (690, my + 30))
				screen.blit(get_text(str(score_shown)), (690, sy + 30))
				
			if self.phase == PHASE_FADE_OUT:
				self.black.set_alpha(int(255 * progress))
				screen.blit(self.black, (0, 0))
				
		