import sys
import re
import pygame
from time import sleep
from player_ship import Ship
from settings import Settings
from bullet import Bullet
from aliens import Alien
from game_stats import GameStats
from button import Button
from mode_button import ModeButton
from scoreboard import Scoreboard
class AlienInvasion:
	"""Overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game, and create game resources"""
		pygame.init() # 1
		self.settings = Settings()
		# Set the Screen
		self.screen = pygame.display.set_mode((0, 0 ), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#Create an instance to store game statisitcs,
		#and create a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#Make play, easy, hard, impossible button
		self.play_button = Button(self, "Play")
		self.easy_button = ModeButton(self,"Easy", self.settings.screen_width /
		3,  (self.settings.screen_height/4) * 3,48, 1 )
		self.hard_button = ModeButton(self, "Hard", self.settings.screen_width /
		2, (self.settings.screen_height/4) * 3, 48, 1)
		self.impossible_button = ModeButton(self, "Impossible", (self.settings.screen_width/3)
		* 2,  (self.settings.screen_height/4) * 3, 48)

		#Set mode values
		self.easy_mode = 0 
		self.hard_mode = 0
		self.impossible_mode = 0
		self.play_on = 0

	def run_game(self):
		"""Start the main loop for the game"""
		while True: # 
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()




	def _check_events(self):
		"""Respond to keypresses and move events"""
		for event in pygame.event.get(): # 4
			if event.type == pygame.QUIT: # 5
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play"""
		button_clicked_play = self.play_button.rect.collidepoint(mouse_pos)
		button_clicked_easy = self.easy_button.rect.collidepoint(mouse_pos)
		button_clicked_hard = self.hard_button.rect.collidepoint(mouse_pos)
		button_clicked_impossible = self.impossible_button.rect.collidepoint(mouse_pos)

		if button_clicked_easy:
			self.easy_mode = 1
			self.stats.game_mode = True
		elif button_clicked_hard:
			self.hard_mode = 1
			self.stats.game_mode = True
		elif button_clicked_impossible:
			self.impossible_mode = 1
			self.stats.game_mode = True
		elif button_clicked_play:
			self.play_on = 1


		if self.play_on and not self.stats.game_active and(self.easy_mode or self.hard_mode or self.impossible_mode):
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			#Reset game statistics
			self.stats.reset_stats()
			self.sb.prep_score()
			self.stats.game_active = True

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()
			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()
			# Hide the mouse cursor
			pygame.mouse.set_visible(False)


		


	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			#Move the ship to the right
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		self.bullets.update()

			#Get rid of bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Respond to bullet-alien collisions"""
		#Check for any bullets that have hit aliens
		# If so, get rid of the bullets and the alien
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens, True, True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
				self.sb.prep_score()
				self.sb.check_high_score()
		if not self.aliens:
			#Destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			#Increase level
			self.stats.level += 1
			self.sb.prep_level()
			if self.easy_mode:
				self.settings.increase_speed_easy()
			elif self.hard_mode:
				self.settings.increase_speed_hard()
			else:
				self.settings.increase_speed_impossible()


	def _ship_hit(self):
		"""Respond to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
			# Decrement ships_left
			self.stats.ships_left -= 1
			self.sb.prep_ships()
	
			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()
	
			#Pause
			sleep(0.5)
		else:
			with open('highscore.txt', 'r+') as file_object:
				highscore = file_object.read()
				if int(highscore) < self.stats.high_score:
					file_object.seek(0)
					file_object.write(re.sub(r"<string>ABC</string>(\s+)<string>(.*)</string>",r"<xyz>ABC</xyz>\1<xyz>\2</xyz>",str(self.stats.high_score)))
					file_object.truncate()
					
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ship got hit
				self._ship_hit()
				break

	def _update_aliens(self):
		"""Update the positions of all the aliens in the fleet"""
		"""
			Check if the fleet is at an edge,
			then update the position of all the aliens in the fleet
			"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#Look for the aliens hitting the bottom of the screen
		self._check_aliens_bottom()


	def _create_fleet(self):
		"""Create a fleet of aliens"""
		#Spacing between alien is equal to one alien width
		alien = Alien(self)
		alien_width, alien_height  = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)
		#Determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#Create full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				#Create an alien and place it in the row
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropritately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Draw the score information
		self.sb.show_score()

		#Draw the play button if the game is inactive
		if not self.play_on:
			self.play_button.draw_button()
		if not self.stats.game_mode: #Get a mode
			self.easy_button.draw_button()
			self.hard_button.draw_button()
			self.impossible_button.draw_button()
				
		pygame.display.flip()



if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()
	
