import random
import pygame
class Food:
	pos = []
	def __init__(self, sgame):
		self.settings = sgame.settings
		self.screen = sgame.screen
		self.color = self.settings.food_color
		self.snake_body = sgame.snake.snake_body

	def draw_food(self, change_position=True):
		while change_position:
			while len(self.pos) > 0:
				self.pos.pop()
			x = random.randint(0, self.settings.num_rows - 1)
			y = random.randint(0, self.settings.num_rows - 1)
			self.pos.append(x)
			self.pos.append(y)
			#We create a simple lambda fuction to go through every 
			#position of the snake body and if the len of that is greater than 0
			#we know that the food is on top of one of its body and we run it again 
			if len(list(filter(lambda position: position.pos == self.pos, self.snake_body))) > 0:  
				continue
			else: 
				break
		spaces = self.settings.spaces #Similar to the draw function we used to draw the blocks
		pygame.draw.rect(self.screen, self.settings.food_color, (self.pos[0]*spaces + 1, self.pos[1]*spaces + 1, spaces-2, spaces-2))
		










