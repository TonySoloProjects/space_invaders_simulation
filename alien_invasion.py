# Python Crash Course Project 1. Alien Invasion
# Created 2020-04-16
# Last modified 2020-04-16
# Ported from Sublime to PyCharm on 4/19/20
# Uploaded to Github 2020-04-30

import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()
		if self.settings.full_screen_mode:
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.settings.screen_width = self.screen.get_rect().width
			self.settings.screen_height = self.screen.get_rect().height
		else:
			self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion MFs!")

		# Create an instance to store game statistics,
		#   and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Make the Play button.
		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Start the main loop for the game."""
	
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			self._update_screen()

	def _check_events(self):
		# Watch fo keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print('You left the battlefield!')
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			# Reset the game statistics.
			self.settings.initialize_dynamic_settings()
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			# get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""Responds to the keypresses."""
		if event.key == pygame.K_q:
			sys.exit()

		if self.stats.game_active:
			if event.key == pygame.K_SPACE:
				self._fire_bullet()
			elif event.key == pygame.K_RIGHT:
				self.ship.moving_right = True
			elif event.key == pygame.K_LEFT:
				self.ship.moving_left = True

	def _check_keyup_events(self, event):
		"""Responds to the key releases."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update bullet positions and get rid of old bullets"""
		self.bullets.update()  # update locations

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		# print(len(self.bullets))

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions."""
		# Check for any bullets that have hit aliens.
		# If so, get rid of the bullet and the alien
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		# Repopulate fleet if you have no aliens left
		if not self.aliens:
			# Clear existing bullets and create a new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			# Increase Level
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""Update alien positions"""
		self.aliens.update()  # march horizontally

		if self._check_fleet_edges(): 		     # check to see if you need to march down and change directions
			self.settings.fleet_direction *= -1  # change direction
			for alien in self.aliens:
				alien.march_down()

		# Look for ship/alien collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _ship_hit(self):
		"""Respond to the ship being hit"""

		if self.stats.ships_left > 0:
			# Update screen so you can see the hit
			self._update_screen()
			# Pause.
			sleep(0.5)

			# Decrement ships_left and update the scoreboard.
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			# Create fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()
		else:
			self.stats.game_active = False
			# Show the mouse cursor.
			pygame.mouse.set_visible(True)

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
				print(f"The aliens got to the bottom!")
				self._ship_hit()
				break

	def _update_screen(self):
		# Redraw the screen during each pass through the loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the score information
		self.sb.show_score()

		# Draw the play button if the game is inactive.
		if not self.stats.game_active:
			self.play_button.draw_button()

		# Make the most recently drawn screen visible
		pygame.display.flip()

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Make an alien
		alien = Alien(self)
		alien_width = alien.rect.width
		alien_height = alien.rect.height

		# Determine the number of aliens per row
		ship_height = self.ship.rect.height
		available_space_x = self.settings.screen_width - 2 * alien_width
		number_aliens_x = available_space_x // (2 * alien_width)

		# Determine the number of rows of aliens that fit on the screen.
		available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
		number_rows = available_space_y // (2 * alien_height)

		# Create the first row of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row"""
		alien = Alien(self)
		(alien_width, alien_height) = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)


if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()
