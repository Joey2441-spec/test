class Settings:
	"""A class to store all settings for Alien Invasion"""

	def __init__(self):
		"""Initialize the game's settings."""
		#Screen Settings
		self.screen_width = None
		self.screen_height = None
		self.bg_color = (230, 230, 230)

		# ship settings
		self.ship_limit = 3

		# bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 10

		#Alien settings 
		self.fleet_drop_speed = 10

		#How quickly the game speeds up
		self.speedup_scale_easy = 1.1
		self.speedup_scale_hard = 1.2
		self.speedup_scale_impossible = 1.5

		#How quickly the aliens point values increase
		self.score_scale = 1.5 

		self.initialize_dynamic_settings()



	def initialize_dynamic_settings(self):
		"""Initialize settings the change throughout the game"""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0
		# fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1
		#Scoring 
		self.alien_points = 50 

	def increase_speed_easy(self):
		"""Increase speed settings"""
		self.ship_speed *= self.speedup_scale_easy
		self.bullet_speed *= self.speedup_scale_easy
		self.alien_speed *= self.speedup_scale_easy
		self.alien_points = int(self.alien_points * self.score_scale)



	def increase_speed_hard(self):
		self.ship_speed *= self.speedup_scale_hard
		self.bullet_speed *= self.speedup_scale_hard
		self.alien_speed *= self.speedup_scale_hard
		self.alien_points = int(self.alien_points * self.score_scale)

	def increase_speed_impossible(self):
		self.ship_speed *= self.speedup_scale_impossible
		self.bullet_speed *= self.speedup_scale_impossible
		self.alien_speed *= self.speedup_scale_impossible
		self.alien_points = int(self.alien_points * self.score_scale)