import math

import pygame

from .fg_element import FGElement


class Sprite(FGElement):
    def __init__(self, image, x=0, y=0, angle=0, velocity=0, move_x=0, move_y=0):
        super().__init__(x=x, y=y, angle=angle, velocity=velocity, move_x=move_x, move_y=move_y)
        self.image = pygame.image.load(image).convert_alpha() if isinstance(image, str) else image
        self._calculate_bounding_radius()

    def draw(self, screen):
        diameter = self.bounding_radius * 2
        s = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(s, (128, 0, 128, 128), (self.bounding_radius, self.bounding_radius), self.bounding_radius)
        screen.blit(s, (self.x - self.bounding_radius, self.y - self.bounding_radius))

    def _calculate_bounding_radius(self):
        w, h = self.image.get_size()
        self.bounding_radius = int(math.sqrt((w ** 2) + (h ** 2)) / 2)
