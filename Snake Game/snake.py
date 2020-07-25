import pygame


class Block:
	"""Blocks that make up the snake's body"""
	def __init__(self, sgame, start):
		self.settings = sgame.settings
		self.screen = sgame.screen
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = self.settings.snake_color

	def move (self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self):
		i = self.pos[0]
		j = self.pos[1]
		spaces = self.settings.spaces
		pygame.draw.rect(self.screen, self.settings.snake_color, (i*spaces + 1, j*spaces + 1, spaces-2, spaces-2))





class Snake:
	"""The snake's body"""
	snake_body = [] # Store snakes body as a list of Block objects
	turns = {} #Keep track of the turns so all the blocks are able to turn at that point 
	def __init__(self, sgame, pos):
		self.sgame = sgame
		self.settings = sgame.settings
		self.screen = sgame.screen
		self.snake_head = Block(sgame, pos)
		self.snake_body.append(self.snake_head)
		self.dirnx = 1 # -1 means left, 0 means nothing, 1 means right
		self.dirny = 0 # 1 means down, 0 means nothing, -1 means up

		
	def move(self):
		for index, block in enumerate(self.snake_body):  # we get the index and block object from list
			position = block.pos[:]  # we set a variable to equal the blocks position
			if position in self.turns:  #if the position equals a key value in the dictionary
				turn = self.turns[position] #we access the value which is the direction that the snake moved
				block.move(turn[0], turn[1])
				if index == len(self.snake_body) - 1: # if we are at the last element of the snake then remove the key value because it's not needed anymore
					self.turns.pop(position)

			else: 
				if block.dirnx == -1 and block.pos[0] <= 0: block.pos = (self.settings.num_rows, block.pos[1])  #Once the snake is at the very left we wrap it to the Right
				elif block.dirnx == 1 and block.pos[0] >= self.settings.num_rows - 1 : block.pos = (0, block.pos[1]) # edge right we wrap to the left
				elif block.dirny == 1 and block.pos[1] >= self.settings.num_rows - 1: block.pos = (block.pos[0], 0) # edge bottom to top
				elif block.dirny == -1 and block.pos[1] <= 0: block.pos = (block.pos[0], self.settings.num_rows)# edge top to bottom
				else: block.move(block.dirnx, block.dirny) #block will move the same direction that it was moving before

	def add_block(self):
		tail = self.snake_body[-1] #Take the last element of the snake
		dirnx = tail.dirnx  #store both last direction that it was moving
		dirny = tail.dirny

		if dirnx == 1 and dirny == 0:  # moving right
			self.snake_body.append(Block(self.sgame,(tail.pos[0] - 1, tail.pos[1]))) # we add the tail to the left side of the last block
		elif dirnx == 0 and dirny == 1: #moving down
			self.snake_body.append(Block(self.sgame,(tail.pos[0], tail.pos[1] - 1))) # we add to the top of the tail
		elif dirnx == -1 and dirny == 0: # moving left 
			self.snake_body.append(Block(self.sgame,(tail.pos[0] + 1, tail.pos[1]))) # we add to the right
		elif dirnx == 0 and dirny == -1: #moving up
			self.snake_body.append(Block(self.sgame,(tail.pos[0], tail.pos[1] + 1))) # we add it to the bottom of the last

		self.snake_body[-1].dirnx = dirnx    #the direction of the new block will equal the second to last block
		self.snake_body[-1].dirny = dirny






	def update(self):
		for index, block in enumerate(self.snake_body):
			block.draw()







