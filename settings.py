from color_dictionary import ColorDictionary as cc

class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""

		# Screen settings.
		# If full_screen_mode=TRUE, then the screen width, height will be determined at runtime
		# Otherwise, the game will use the width and height specified below
		self.full_screen_mode = False
		self.screen_width = 1080
		self.screen_height = 720
		self.bg_color = cc.color['lighter gray']  # Medium Grey Background (230, 230, 230)

		# Ship settings
		self.ship_limit = 2  # Number of additional ships at startup

		# Bullet settings
		self.bullet_width = 3  # make wider to speed up debugging
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5  # Max bullets on screen at any given time

		# Alien settings
		self.fleet_drop_speed = 10  # How far the aliens march down when they hit a lateral edge (10)

		# How quickly the game speeds up at the completion of each level.
		self.speedup_scale = 1.1

		# How quickly the alien point value increase at the completion of each level.
		self.score_scale = 1.5

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout time"""

		# Direction fleet will start marching, initially to the right
		self.fleet_direction = 1.0  # +1 if going right, -1 if going left

		# Variables that will be increased at the end of a level
		self.ship_speed = 1.5
		self.bullet_speed = 3
		self.alien_speed = 0.6
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings at the completion of a level"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
