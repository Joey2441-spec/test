class Settings:
	"""Settings for snake game"""
	def __init__(self):

		#Design of the Map
		self.screen_size = 500		#Allows you to mess with the screen and adjust the game 
		self.bg_color = (0, 0, 0) 
		self.spaces = 25
		self.num_rows = int(self.screen_size / self.spaces)
		#Design of the snake, food
		self.snake_size = 25
		self.snake_color = (0, 255, 0)
		self.food_color = (255, 0, 0)
