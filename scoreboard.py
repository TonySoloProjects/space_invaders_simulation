import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize score-keeping attributes"""

        # Shortcut variables for main game screen, settings, and stats
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font setting for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score, level, and ship count
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""

        # rounded_score = round(self.stats.score, -1)  # Round to the nearest 10s
        rounded_score = self.stats.score  # Score not rounded
        score_str = "{:,}".format(rounded_score)

        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image"""

        # high_score = round(self.stats.high_score, -1)  # Round to the nearest 10s
        high_score =self.stats.high_score  # Score not rounded 

        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Position the score at the top center of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.score_rect.top
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        """Turn the level into a rendered image"""

        level_str = f"L {self.stats.level}"

        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level to the top left.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.level_rect.bottom + 20

    def prep_ships(self):
        """Show how many ships are remaining graphically
           by showing ship images in the top left."""

        # Group is a pygame way to organize Sprites
        self.ships = Group()

        # Put the remaining ships in the top left with a little spacing
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score, high score, level, and remaining ships to screen."""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""

        # If current game's score is greater than high score then update the high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
