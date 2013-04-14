# I'll do this later after we have oggs

class JukeBox:
	def __init__(self):
		self.now_playing = None
	
	def play(self, song):
		file = 'music' + os.sep + song + '.mp3'