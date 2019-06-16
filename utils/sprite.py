import math
import weakref

import pygame

from .fg_element import FGElement


class Sprite(FGElement):
    def __init__(self, image, x=0, y=0, angle=0, velocity=0, move_x=0, move_y=0):
        super().__init__(x=x, y=y, angle=angle, velocity=velocity, move_x=move_x, move_y=move_y)
        self.image = pygame.image.load(image).convert_alpha() if isinstance(image, str) else image
        self.collider = Collider(self)

    def draw(self, screen):
        self.collider.draw(screen)


class Collider:
    def __init__(self, sprite):
        self.sprite = weakref.ref(sprite)
        self.update_dims()

    def draw(self, screen):
        diameter = self.radius * 2
        s = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(s, (128, 0, 128, 128), (self.radius, self.radius), self.radius)
        screen.blit(s, (self.sprite().x - self.radius, self.sprite().y - self.radius))

    def center(self):
        bounds_x, bounds_y = self.bounds
        return self.sprite().x - bounds_x, self.sprite().y - self.bounds_y

    def update_dims(self):
        bounds_x, bounds_y = self.bounds = self.sprite().image.get_size()
        # NOTE: take 80% of true radius to give collisions some fudge-factor
        self.radius = int((math.sqrt((bounds_x ** 2) + (bounds_y ** 2)) / 2) * 0.8)

    def collide(self, collider):
        pass
