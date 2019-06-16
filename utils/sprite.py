import math
import weakref

import pygame

from .fg_element import FGElement


class Sprite(FGElement):
    def __init__(self, image, x=0, y=0, angle=0, velocity=0, move_x=0, move_y=0):
        super().__init__(x=x, y=y, angle=angle, velocity=velocity, move_x=move_x, move_y=move_y)
        self.image = pygame.image.load(image).convert_alpha() if isinstance(image, str) else image
        self.collider = Collider(self)

    def update(self, model, lag_scalar):
        self.collider.visible = model.show_colliders

    def draw(self, screen):
        self.collider.draw(screen)


class Collider:
    def __init__(self, sprite):
        self.collided = self.visible = False
        self.sprite = weakref.ref(sprite)
        self.update_size()

    @property
    def center(self):
        return int(self.sprite().x - self.radius), int(self.sprite().y - self.radius)

    def draw(self, screen):
        if not self.visible:
            return
        diameter = self.radius * 2
        s = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        color = (255, 255, 0, 128) if self.collided else (128, 0, 128, 128)
        c_x, c_y = self.center
        pygame.draw.circle(s, color, (self.radius, self.radius), self.radius)
        screen.blit(s, self.center)

    def update_size(self):
        bounds_x, bounds_y = self.sprite().image.get_size()
        # NOTE: take 80% of true radius to give collisions some fudge-factor
        self.radius = int((math.sqrt((bounds_x ** 2) + (bounds_y ** 2)) / 2) * 0.8)

    def collide(self, collider):
        my_x, my_y = self.center
        their_x, their_y = collider.center
        a = my_x - their_x
        b = my_y - their_y
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < (self.radius + collider.radius):
            self.collided = collider.collided = True
