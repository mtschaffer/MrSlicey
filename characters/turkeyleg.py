import math
import os

import pygame

from camera.camera import camera
from scene.score_board import ScoreBoard
from utils.audio import audio
from utils.sprite import Sprite, Collider
from utils.collision import CollisionEffect


IMAGE_PATH = os.path.join('images', 'turkeyleg.png')
IMAGE = pygame.image.load(IMAGE_PATH).convert_alpha()


class TurkeyLeg(Sprite):
    def __init__(self, x, y, angle, rotational_velocity, idx):
        super().__init__(
            image=IMAGE,
            x=x,
            y=y,
            angle=angle,
            velocity=1,
            move_x=0,
            move_y=0
        )

        self.idx = idx

        self.flame_image = pygame.image.load(os.path.join('images', 'flame.png')).convert_alpha()

        self.acceleration = 0.5
        self.max_velocity = 10.0
        self.move_velocity = 0

        self.set_orientation_vector()

        self.rotational_velocity = rotational_velocity
        self.destroyed = False
        self.score_board = ScoreBoard.instance()

    def set_orientation_vector(self, model=None):
        self.orientation_vector_x = math.sin(math.radians(self.angle))
        self.orientation_vector_y = math.cos(math.radians(self.angle))

        if model:
            if self.idx % 2 == 0:
                self.orientation_vector_x *= model.orientation_vector_x * .8
                self.orientation_vector_y *= model.orientation_vector_y * .8
            else:
                self.orientation_vector_x *= model.orientation_vector_y * .8
                self.orientation_vector_y *= model.orientation_vector_x * .8

            if self.idx % 6 == 0:
                self.orientation_vector_x = model.orientation_vector_x - self.orientation_vector_x
                self.orientation_vector_y = model.orientation_vector_y - self.orientation_vector_y

    def get_wrekt(self, model):

        if self.idx % 2 == 0:
            return math.sqrt((self.orientation_vector_x ** 2) + (self.orientation_vector_y ** 2)) * (1 / (model.velocity or 1))
        else:
            return math.sqrt((self.orientation_vector_x ** 2) + (self.orientation_vector_y ** 2)) * 1.3

    def create_collider(self):
        return Collider(self, effect=CollisionEffect.Halt, reaction=self.collided)

    def collided(self, collider, effect):
        if effect == CollisionEffect.Destroy:
            self.score_board.incr_score(1)
            self.destroyed = True
        elif effect == CollisionEffect.Halt:
            pass    # do nothing if colliding with a fellow halter
        else:
            collider.collided = True

    def update(self, model, lag_scalar):
        super().update(model, lag_scalar)
        self.angle += (self.rotational_velocity * lag_scalar)
        self.angle %= 360

        devious = model.watermelon
        self.set_orientation_vector(devious)

        self.velocity = max(min(self.max_velocity, self.velocity + self.get_wrekt(devious)), -self.max_velocity)

        self.move_x = self.velocity * self.orientation_vector_x
        self.move_y = self.velocity * self.orientation_vector_y

        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

        if self.destroyed:
            audio.play_any_sfx('drumstick1', 'drumstick2')
            model.remove_fg_element(self)

    def draw(self, screen):
        super().draw(screen)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        w, h = rotated_image.get_size()
        camera.blit(rotated_image, (self.x - w / 2, self.y - h / 2))
