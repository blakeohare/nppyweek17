import os


chars = 'superman batman riddler joker'.split()
directions = 'down left up right'.split()

output = []
for char in chars:
	c = open(char + '.png', 'rb')
	t = c.read()
	c.close()
	for d in directions:
		file = char + '_standing_' + d + '.png'
		output.append((file, t))
		for i in '1 2 3'.split():
			output.append((char + '_walking_' + d + '_' + i + '.png', t))


for x in output:
	c = open(x[0], 'wb')
	c.write(x[1])
	c.close()
	