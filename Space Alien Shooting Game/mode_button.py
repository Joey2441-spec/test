import pygame.font

class ModeButton:
	"""Creates the settings for an easy button game mode"""
	def __init__(self, ai_game, msg, x, y, size, center = 0):
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#Initialize button properties
		self.center = center
		self.width, self.height = 200, 50
		self.button_color = (150, 80, 150)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, size )

		#Build buttons rect/surface to where the writing will be placed on
		self.rect = pygame.Rect(0,0, self.width, self.height)
		self.rect.x = x - (self.width / 2)
		self.rect.y = y 

		self._prep_msg(msg)

	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button"""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		if self.center:
			self.msg_image_rect.x = self.rect.x + (self.width / 4)		#Center the text
		else:
			self.msg_image_rect.x = self.rect.x
		self.msg_image_rect.y = self.rect.y

	def draw_button(self):
		#Draw button for modes
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
