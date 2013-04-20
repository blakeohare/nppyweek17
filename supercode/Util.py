import pygame
import os

_sound_id_to_file = {
	'init': False,
	'incorrect_order': 'nobad',
	'cant_drop_box': None,
	'money_sound': 'chaching',
	'lift': 'pickup',
	'drop': 'putdown',
	'click': 'click',
	'funny1': 'ninini',
	'funny2': 'glub',
	'funny3': 'shapeshifter',
	'funny4': 'buzz',
}

def play_sound(id):
	lookup = _sound_id_to_file
	if not lookup['init']:
		for key in lookup.keys():
			if key != 'init' and lookup[key] != None:
				path = "sound/" + lookup[key] + '.ogg'
				path = path.replace('/', os.sep)
				lookup[key] = pygame.mixer.Sound(path)
		lookup['init'] = True
	
	snd = lookup[id]
	if snd != None:
		snd.play()

_images2x = {}
_images = {}
def get_image(path):
	img = _images.get(path, None)
	if img == None:
		canonical_path = path.lower().replace('\\', '/')
		if not canonical_path.endswith('.png') and not canonical_path.endswith('.jpg'):
			canonical_path += '.png'
		if canonical_path[0] == '/':
			canonical_path = canonical_path[1:]
		if not canonical_path.startswith('images/'):
			canonical_path = 'images/' + canonical_path
		canonical_path = canonical_path.replace('/', os.sep).replace('\\', os.sep)
		
		img = pygame.image.load(canonical_path)
		
		if canonical_path.startswith('images/tiles/') and not ('walltop' in canonical_path):
			img = img.convert()
		_images[path] = img
		_images[canonical_path] = img
	return img

def get_image_2x(path, scale):
	rpath = str(scale) + '|' + path
	img = _images2x.get(rpath, None)
	if img == None:
		t = get_image(path)
		img = pygame.transform.scale(t, (t.get_width() * scale, t.get_height() * scale))
		_images2x[rpath] = img
	return img

def legacy_map(function, items):
	output = []
	for item in items:
		output.append(function(item))
	return output

def trim(string):
	if string == None: return ''
	while len(string) > 0 and string[0] in ' \r\n\t':
		string = string[1:]
	while len(string) > 0 and string[-1] in ' \r\n\t':
		string = string[:-1]
	return string


_letter_lookup = {
	':': 'colon',
	',': 'comma',
	'$': 'dollar',
	'!': 'excl',
	'.': 'period',
	'?': 'ques',
	"'": 'apostrophe',
	'"': 'quote',
	'-': 'hyphen',
	'<': 'lessthan',
	'>': 'greaterthan',
	'*': 'asterisk',
	'@': 'at',
	'=': 'equals',
	'_': 'underscore',
	'#': 'hash',
	'^': 'caret',
	'(': 'openparen',
	')': 'closeparen',
	'%': 'percent',
	'+': 'plus',
	';': 'semicolon',
	'/': 'slash'
}
for c in 'abcdefghijklmnopqrstuvwxyz':
	_letter_lookup[c] = c
	_letter_lookup[c.upper()] = c
for c in range(10):
	_letter_lookup[str(c)] = 'num' + str(c)
_letters = {}
def char_to_img(char):
	img = _letters.get(char, None)
	if img == None:
		if char == ' ':
			sps = char_to_img('n')
			img = pygame.Surface(sps.get_size(), pygame.SRCALPHA) # blank image the size of the 'N' image
		else:
			t = _letter_lookup.get(char, 'ques')
			img = get_image('font/' + t)
		_letters[char] = img
	return img

def max(a, b):
	if a > b: return a
	return b

def min(a, b):
	if a < b: return a
	return b

def mouse_x():
	return pygame.mouse.get_pos()[0]

def mouse_y():
	return pygame.mouse.get_pos()[1]

_text_cache = {}
def get_text(text, small=False):
	key = str(small)[0] + text
	img = _text_cache.get(key)
	if img == None:
		letters = []
		width = 0
		height = 0
		for char in text:
			c = char_to_img(char)
			letters.append(c)
			width += c.get_width()
			height = max(height, c.get_height())
		img = pygame.Surface((width, height), pygame.SRCALPHA)
		x = 0
		for char in letters:
			img.blit(char, (x, 0))
			x += char.get_width()
		if small:
			img = pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
			img.blit(img, (0, 0))
		_text_cache[key] = img
	return img

def get_small_text(text):
	return get_text(text, True)

def format_money(amount, use_cents=True):
	if amount == 0:
		if use_cents:
			return "$0.00"
		return "$0"
	s = str(amount)
	output = []
	while len(s) > 0:
		t = s[-3:]
		s = s[:-3]
		output = [t] + output
	
	output = '$' + ','.join(output)
	if use_cents:
		output += '.00'
	return output


def is_over_plot(plot):
	if plot == None: return False
	mx = mouse_x()
	my = mouse_y()
	if mx >= plot[0] and my >= plot[1]:
		if mx <= plot[0] + plot[2]:
			if my <= plot[1] + plot[3]:
				return True
	return False

def get_arrow(direction, is_blinking, counter):
	if not is_blinking or (((counter // 3) % 2) == 0):
		return get_image('misc/' + direction + '_arrow_small')
	return get_image('misc/' + direction + '_arrow')
	