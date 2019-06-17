import os

import pygame

from utils.sprite import Sprite, Collider
from utils.collision import CollisionEffect


IMAGE_PATH = os.path.join('images', 'turkeyleg.png')
IMAGE = pygame.image.load(IMAGE_PATH).convert_alpha()


class TurkeyLeg(Sprite):
    def __init__(self, x, y, angle, rotational_velocity):
        super().__init__(
            image=IMAGE,
            x=x,
            y=y,
            angle=angle,
            velocity=0,
            move_x=0,
            move_y=0
        )
        self.rotational_velocity = rotational_velocity
        self.destroyed = False

    def set_collider(self):
        self.collider = Collider(self, effect=CollisionEffect.Halt, reaction=self.collided)

    def collided(self, collider, effect):
        if effect == CollisionEffect.Destroy:
            self.destroyed = True
        else:
            collider.collided = True

    def update(self, model, lag_scalar):
        super().update(model, lag_scalar)
        self.angle += (self.rotational_velocity * lag_scalar)
        self.angle %= (360 if self.angle > 0 else -360)
        if self.destroyed:
            model.remove_fg_element(self)

    def draw(self, screen):
        super().draw(screen)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        w, h = rotated_image.get_size()
        screen.blit(rotated_image, (int(self.x - w / 2), int(self.y - h / 2)))
