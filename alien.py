import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in a fleet"""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()

        # Shortcut variables to main gaming object
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the alien image and save its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Initially position each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact location as a float to enable smooth movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the position based on the movement direction."""

        # Find the new horizontal position based on float calculations
        self.x += self.settings.alien_speed * self.settings.fleet_direction

        # update rect object from self.x
        self.rect.x = self.x

    def check_edges(self):
        """Returns true if an alien is at the edge of the screen"""

        if (self.rect.right >= self.screen_rect.right) \
                or (self.rect.left <= 0):
            return True
        else:
            return False

    def march_down(self):
        """March alien downwards"""
        # This function is called when a member of the fleet gets to a left/right edge
        self.rect.y += self.settings.fleet_drop_speed
