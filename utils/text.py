import pygame

from utils.fg_element import FGElement

WHITE = (0xFF, 0xFF, 0xFF)

class Text(FGElement):
    def __init__(self, text, x, y, center=False):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.rendered_font = self.font.render(self.text, True, WHITE)

        if center:
            self.x -= self.rendered_font.get_width() / 2

    def draw(self, screen):
        screen.blit(self.rendered_font, (int(self.x), int(self.y)))
