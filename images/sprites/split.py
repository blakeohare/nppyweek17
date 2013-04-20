import pygame
import os

pygame.init()
characters = 'player villain1 hero1 villain2 hero2'.split()

for character in characters:
	img = pygame.image.load(character + '.png')



	cols = '$_*_down $_*_up $_*_left $_*_right $_hold_*_down $_hold_*_up $_hold_*_left $_hold_*_right'.replace('$', character).split()
	rows = 'standing walking_1 walking_2 walking_3 walking_4'.split()

	width = 16
	height = 32

	x = 0
	for col in cols:
		y = 0
		for row in rows:
			file = None
			parts = row.split('_')
			action = parts[0]
			if len(parts) == 2:
				num = str(parts[1])
			else:
				num = None
			
			file = col.replace('*', action)
			if num != None:
				file += '_' + num
			file += '.png'
			
			output = pygame.Surface((16, 32), pygame.SRCALPHA)
			output.blit(img, (-x, -y))
			print file, output
			pygame.image.save(output, 'foo\\' + file)
			y += height
		x += width