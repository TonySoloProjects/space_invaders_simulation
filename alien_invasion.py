# Python Crash Course Project 1. Alien Invasion
# Created 2020-04-16
# Last modified 2020-05-07
# Uploaded to Github 2020-05-04

import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from button import MultiLineMessage
from scoreboard import Scoreboard
from color_dictionary import ColorDictionary as cc


class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""

		self.settings = Settings()  # Global game settings

		# Initialize pygame and create gaming surface window
		pygame.init()
		if self.settings.full_screen_mode:
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.settings.screen_width = self.screen.get_rect().width
			self.settings.screen_height = self.screen.get_rect().height
		else:
			self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion MFs!")

		# Create an instance to store game statistics,
		# and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		# Create ship, bullets, and alien sprites
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		# Store sound effects
		self.bullet_sound = pygame.mixer.Sound('sounds/shoot.wav')
		self.bullet_sound.set_volume(0.1)
		self.invader_sound = pygame.mixer.Sound('sounds/invaderkilled.wav')
		self.invader_sound.set_volume(0.1)
		self.ship_explode_sound = pygame.mixer.Sound('sounds/explosion2.wav')
		self.bullet_sound.set_volume(0.2)


		# Create intro text
		intro_text = [
			"Alien Invaders - Enter if you dare!",
			"Spacebar to start.",
			"Press 'q' to quit."]
		self.intro_button = MultiLineMessage(self, intro_text, 600, 175)

		level_text = [
			"Level 1",
			"Aliens worth xx Points"]

	def run_game(self):
		"""Start the main loop for the game."""

		# Run indefinitely until the user quits or closes
		while True:
			# check for keyboard and mouse events
			self._check_events()

			# If game is actively being played, update the sprites
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			# update the main screen based on sprite activity
			self._update_screen()

	def _check_events(self):
		"""Listen for and then process keyboard and mouse events."""

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()  # user ends game by closing window with mouse click
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_intro_button(mouse_pos)

	def _check_keydown_events(self, event):
		"""Responds to the keypresses."""

		# pressing q stops the game at any time
		if event.key == pygame.K_q:
			sys.exit()  # user ends game by typing q

		# If game is active, keyboard moves ship and fires bullet
		# If game is not active, pressing spacebar starts the game
		if self.stats.game_active:
			if event.key == pygame.K_SPACE:
				self._fire_bullet()
			elif event.key == pygame.K_RIGHT:
				self.ship.moving_right = True
			elif event.key == pygame.K_LEFT:
				self.ship.moving_left = True
		else:
			if event.key == pygame.K_SPACE:
				pygame.mouse.set_visible(False)  # Hide the mouse cursor.
				self._reset_stats_for_display()
				self._start_level()

	def _start_level(self, advance_level=False):
		"""Reset sprites, and statistics and prepare to play level"""

		if advance_level:
			# Increase Level
			self.stats.level += 1
			self.settings.increase_speed()
			self.sb.prep_level()

		self._reset_sprites()
		self._ready_player_one()

	def _ready_player_one(self):
		"""Inform game starting/resuming and display level and alien point values"""

		level_text = [	f"On Level {self.stats.level}.",
						f"Aliens worth {self.settings.alien_points} points.",
						"Ready Player One!"	]
		self._display_text(level_text, 425, 175, 2)

	def _game_over(self):
		"""Sad Tuba, Inform the player that the game is over"""

		level_text = [f"Game Over!"]
		self._display_text(level_text, 235, 75, 1.5, False)

	def _display_text(self, text, width, height, sleep_time, update_game_elements=True):
		"""Display message box to inform player"""

		if update_game_elements:
			# Show the sprites for the new level
			self._update_gaming_elements()
			pygame.display.flip()

		# Render text to messagebox and display for brief time
		level_message = MultiLineMessage(self, text, width, height)
		level_message.draw_button()
		pygame.display.flip()
		sleep(sleep_time)

	def _check_keyup_events(self, event):
		"""Responds to the key releases."""

		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		"""Add a bullet if you are less than the max bullets"""

		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
			self.bullet_sound.play()

	def _update_bullets(self):
		"""Update bullet positions, get rid of old bullets, and check for aliens shot down"""

		self.bullets.update()  # update locations

		# Get rid of bullets that have moved past the top of the screen.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		# print(len(self.bullets))

		# Remove bullets that collided with aliens
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions.
		   Remove bullets and aliens that are hit and update the score(s)."""

		# Check for any bullets that have hit aliens.
		# If so, get rid of the bullet and the alien
		# Note: if a bullet is wide enough, it can hit multiple aliens
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if collisions:
			# If you have very wide bullets, you can hit multiple aliens at a time
			# len(aliens) is the number of aliens hit with a single bullet
			self.invader_sound.play()
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		# Repopulate fleet and advance the level if you have no aliens left
		if not self.aliens:
			self._start_level(advance_level=True)

	def _update_aliens(self):
		"""Update alien positions"""

		self.aliens.update()  # move horizontally

		if self._check_fleet_edges(): 		     # check to see if you hit an edge
			self.settings.fleet_direction *= -1  # change direction of horizontal movement
			for alien in self.aliens:            # move the alien fleet down
				alien.march_down()

		# Look for ship/alien collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_lost()
			return

		# Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _ship_lost(self):
		"""Respond to the ship being lost by it being hit or the aliens get to the bottom"""

		if self.stats.ships_left > 0:
			self._explode_and_pause(1.0)

			# Decrement ships_left and update the scoreboard.
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Restart the same level with a new fleet
			self._start_level()
		else:
			self._explode_and_pause(0.75)
			self._game_over()
			self.stats.game_active = False
			# remove all the events from the last game
			# if you don't, a lingering spacebar hit may start a new game
			pygame.event.clear()

			# Show the mouse cursor.
			pygame.mouse.set_visible(True)

	def _explode_and_pause(self, pause_in_seconds):
		"""Explode the ship and pause to let the gravity of the moment sink in :) """
		# Update screen so you can see last game board
		# put an exploded ship on the old ship
		self.ship_explode_sound.play()
		self._update_screen()
		self.ship.explode_ship()
		pygame.display.flip()
		sleep(pause_in_seconds)

	def _check_fleet_edges(self):
		"""Return true if an alien touches an left/right edge"""

		edge_touch = False
		for alien in self.aliens:
			if alien.check_edges():
				edge_touch = True
				break
		return edge_touch

	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""

		screen_rect = self.screen.get_rect()
		for alien in self.aliens:
			if alien.rect.bottom >= screen_rect.bottom:
				#  print(f"The aliens got to the bottom!")
				self._ship_lost()
				break

	def _update_screen(self):
		"""Redraw the screen refreshing all content.
		   Start by drawing background color to screen which wipes the slate clean.
		   Then populate all the gaming elements (sprites, scores, ect).
		   Lastly, display message box to allow the player to play/restart
		   Note that the rendering is done to the screen surface that is only made
		   visible to the user when the .flip routine is called to make movement smoother."""

		self._update_gaming_elements()

		# If the game is inactive, draw the intro message box.
		if not self.stats.game_active:
				self.intro_button.draw_button()
				# in case the ship is exploded, put it on the top of the alien
				self.ship.blitme()

		# Make the most recently drawn screen visible
		pygame.display.flip()

	def _update_gaming_elements(self):
		"""Fill surface with background color to reset screen
		   then draw all sprites, scores, levels, and remaining ships."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		# Draw the score & ships remaining
		self.sb.show_score()

	def _create_fleet(self):
		"""Create the fleet of aliens."""

		# Number of aliens per row will leave at least 1 alien width of space on left & right
		# Initial number of rows of aliens will fill the top two thirds of the screen
		# Make an alien
		alien = Alien(self)
		alien_width = alien.rect.width
		alien_height = alien.rect.height

		# Determine the number of aliens per row
		available_space_x = self.settings.screen_width - 2 * alien_width
		number_columns = available_space_x // (2 * alien_width)

		# Determine the number of rows of aliens that fit on the screen.
		ship_height = self.ship.rect.height
		available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)

		# Create the first row of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_columns):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row, column fleet"""

		alien = Alien(self)
		(alien_width, alien_height) = alien.rect.size

		# Include a buffer on the side and one blank space in between each alien
		alien.rect.x = alien_width + 2 * alien_width * alien_number
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

		# Store the horizontal location as a float for smoother motion.
		alien.x = alien.rect.x

		self.aliens.add(alien)

	def _check_intro_button(self, mouse_pos):
		"""Start a new game when the player clicks the intro text."""

		button_clicked = self.intro_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._reset_stats_for_display()
			self._start_level()
			pygame.mouse.set_visible(False)  # Hide the mouse cursor.

	def _reset_sprites(self):
		"""Clear old sprites, create a new fleet, and center ship."""

		self.aliens.empty()
		self.bullets.empty()
		self._create_fleet()
		self.ship.center_ship()
		self.ship.exploded = False

	def _reset_stats_for_display(self):
		"""Prepare the statistics, text, and ship remaining information for first time of play."""

		self.stats.game_active = True
		self.settings.initialize_dynamic_settings()
		self.stats.reset_stats()
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_ships()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()
