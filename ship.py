import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""

        super().__init__()

        # Shortcut variables to main gaming object and settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.exploded = False  # Determine if the ship should be normal or exploded
        self.ship_alive = pygame.image.load('images/ship.bmp')
        self.ship_dead = pygame.image.load('images/ship-exploded.bmp')
        self.image = self.ship_alive
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        if self.exploded:
            self.screen.blit(self.ship_dead, self.rect)
        else:
            self.screen.blit(self.ship_alive, self.rect)

    def explode_ship(self):
        """Draw the exploded ship at its current location."""
        self.exploded = True
        self.blitme()

    def update(self):
        """Update the position based on the movement flag."""

        # calculate new x location as a float if you don't go off the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship at the bottom of the screen."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
