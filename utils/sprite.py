import pygame

from .fg_element import FGElement


class Sprite(FGElement):
    def __init__(self, image, x=0, y=0, angle=0, velocity=0, move_x=0, move_y=0):
        super().__init__(x=x, y=y, angle=angle, velocity=velocity, move_x=move_x, move_y=move_y)
        self.image = pygame.image.load(image).convert_alpha() if isinstance(image, str) else image
