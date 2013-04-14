import pygame
import os

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
		_images[path] = img
		_images[canonical_path] = img
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

_sound_id_to_file = {
}

# does a lookup between id's and the actual file name
def play_sound(id):
	file = _sound_id_to_file.get(id)
	# TODO: play that file


_letter_lookup = {
	':': 'colon',
	',': 'comma',
	'$': 'dollar',
	'!': 'excl',
	'.': 'period',
	'?': 'ques'
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

_text_cache = {}
def get_text(text):
	img = _text_cache.get(text)
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
		_text_cache[text] = img
	return img
			