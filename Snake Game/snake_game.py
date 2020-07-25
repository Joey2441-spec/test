import pygame
import sys
from settings import Settings
from snake import Block, Snake
from food import Food
class SnakeGame:
	
	def __init__(self): # Pre settings to get the game set up
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((self.settings.screen_size, self.settings.screen_size))
		pygame.display.set_caption("Snake Game")
		self.init_grid = self._draw_grid()
		self.snake = Snake(self, (10,10))
		self.food = Food(self)
		self.food.draw_food()
	def run_game(self): # Main method to help run the game
		while True:
			pygame.time.delay(10)
			pygame.time.Clock().tick(10)
			self._check_key_events()
			self._update_screen()







	def _check_key_events(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					sys.exit()
				elif event.key == pygame.K_RIGHT:
					self.snake.dirnx = 1
					self.snake.dirny = 0
					self.snake.turns[self.snake.snake_head.pos[:]] = [self.snake.dirnx, self.snake.dirny] # Create a new key with the current position of the snake head
																										  # with the values of your direction
				elif event.key == pygame.K_LEFT:
					self.snake.dirnx = -1
					self.snake.dirny = 0
					self.snake.turns[self.snake.snake_head.pos[:]] = [self.snake.dirnx, self.snake.dirny]
				elif event.key == pygame.K_UP:
					self.snake.dirnx = 0
					self.snake.dirny = -1
					self.snake.turns[self.snake.snake_head.pos[:]] = [self.snake.dirnx, self.snake.dirny]
				elif event.key == pygame.K_DOWN:
					self.snake.dirnx = 0
					self.snake.dirny = 1
					self.snake.turns[self.snake.snake_head.pos[:]] = [self.snake.dirnx, self.snake.dirny]


	def _check_body_touch(self):
		"""Use to check if the snake's head is touching it's body"""
		if len(list(filter(lambda position: position.pos == self.snake.snake_body[0].pos, self.snake.snake_body[1:]))) > 0:  # We check if the head position equals to any of the body's position
			print(f"You got a scored of {len(self.snake.snake_body)}!!!") #Print the length of the snake as score
			sys.exit() #Exit the game
			

				
		
	def _update_screen(self): #Update screen
		self.screen.fill((0,0,0))
		self._draw_grid()
		self.snake.move()
		self.snake.update()
		self._check_body_touch()

		#for i in range(len(self.snake.snake_body)):
		if self.food.pos[0] == self.snake.snake_body[0].pos[0] and self.food.pos[1] == self.snake.snake_body[0].pos[1]:
			self.snake.add_block()
			self.food.draw_food()
			
		else:
			self.food.draw_food(change_position=False)
		pygame.display.flip()

	def _draw_grid(self):
		x = 0
		y = 0 
		for block in range(self.settings.num_rows):
			x += self.settings.spaces
			y += self.settings.spaces 

			pygame.draw.line(self.screen, (255, 255, 255), (x,0), (x,self.settings.screen_size)) #Draw the vertical lines on the grid
			pygame.draw.line(self.screen, (255, 255, 255), (0,y), (self.settings.screen_size,y)) #Draw the horizontal lines on the grid






if __name__ == '__main__':
	game = SnakeGame()
	game.run_game()

