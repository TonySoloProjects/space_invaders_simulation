import pygame.font
from color_dictionary import ColorDictionary as cd


class Button:
    """A class to represent a mouse clickable buttons to display information/graphics to the player.
       Implements as a rect object that has a rendered text image placed above it."""

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""

        # Shortcut variables to main gaming object
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = cd.color['orange']
        self.text_color = cd.color['white']
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw solid rect and place message text above to simulate a button"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class MultiLineMessage:
    """A class to represent introduction & level messages to player.
       Implements as a rect object that has a rendered text image placed above it.
       Based on Crash Course button object, but now allows for multiline text."""

    def __init__(self, ai_game, text, width, height):
        """Initialize button attributes."""

        # Shortcut variables to main gaming object
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.text = text
        self.message_images = []   # Surfaces for each rendered line of text
        self.message_recs = []

        self.font_size = 48
        self.line_spacing = 10
        self.width, self.height = width, height
        self.button_color = cd.color['orange']
        self.text_color = cd.color['white']
        self.font = pygame.font.SysFont(None, self.font_size)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(self.text)

    def _prep_msg(self, messages):
        """Turn messages list into a left aligned rendered images.
           Save list and save the rect information to self."""

        for i, message in enumerate(messages):
            message_image = self.font.render(message, True, self.text_color, self.button_color)
            message_rec = message_image.get_rect()
            #message_rec.x = self.rect.left + (self.line_spacing*2)
            message_rec.centerx = self.rect.centerx
            message_rec.y = self.rect.top + (self.line_spacing*2) + 50*i
            self.message_images.append(message_image)
            self.message_recs.append(message_rec)

    def draw_button(self):
        """Draw solid rect and place message text above to display multi-line message"""

        self.screen.fill(self.button_color, self.rect)
        for message, rec in zip(self.message_images, self.message_recs):
            self.screen.blit(message, rec)

