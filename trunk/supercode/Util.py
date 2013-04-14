import pygame
import os

_images = {}
def get_image(path):
	img = _images.get(path, None)
	if img == None:
		canonical_path = path.lower().replace('/', os.sep).replace('\\', os.sep)
		if not canonical_path.endswith('.png') and not canonical_path.endswith('.jpg'):
			canonical_path += '.png'
		if canonical_path[0] == '/':
			canonical_path = canonical_path[1:]
		if not canonical_path.startswith('images/'):
			canonical_path = 'images/' + canonical_path
		img = pygame.image.load(canonical_path)
		_images[path] = img
		_images[canonical_path] = img
	return img

def legacy_map(function, items):
	output = []
	for item in items:
		output.append(function(item))
	return output