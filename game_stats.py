class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize Statistics"""

        # Shortcut variables to settings
        self.settings = ai_game.settings

        # High score starts at zero and is not modified by reset_stats function.
        self.high_score = 0

        self.reset_stats()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game"""

        self.ships_left = self.settings.ship_limit  # Remaining Ships
        self.score = 0  # Game Score
        self.level = 1  # Starting Level
