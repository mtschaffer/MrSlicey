import os
import math

import pygame

from camera.camera import camera
from scene.score_board import ScoreBoard
from utils.sprite import Sprite, Collider

IMAGE_PATH = os.path.join('images', 'watermelon.png')


class Watermelon(Sprite):
    def __init__(self, seed_inventory=0, x=320, y=240, velocity=1.0):
        super().__init__(
            image=IMAGE_PATH,
            x=x,
            y=y,
            angle=180,
            velocity=velocity,
            move_x=0,
            move_y=0
        )
        self.flame_image = pygame.image.load(os.path.join('images', 'flame.png')).convert_alpha()



        self.destroyed = False
        self.score_board = ScoreBoard.instance()

        self.set_orientation_vector()

    def create_collider(self):
        return Collider(self, reaction=self.collided)

    def collided(self, collider, effect):
        pass

    def set_orientation_vector(self):
        self.orientation_vector_x = math.sin(math.radians(self.angle))
        self.orientation_vector_y = math.cos(math.radians(self.angle))

    def draw(self, screen):
        super().draw(screen)
        self.draw_melon(screen)

    def draw_melon(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle - 180)
        w, h = rotated_image.get_size()
        camera.blit(rotated_image, (self.x - w / 2, self.y - h / 2))


