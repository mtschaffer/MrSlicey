import pygame

WHITE = (0xFF, 0xFF, 0xFF)


class Text:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        rendering = self.font.render(self.text, True, WHITE)
        screen.blit(rendering, (int(self.x), int(self.y)))

    def text(self, text):
        self.text = text

    def position(self, x, y):
        self.x = x
        self.y = y
