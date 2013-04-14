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