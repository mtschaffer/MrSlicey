import os

import pygame


class Projectile:

    def __init__(self, image_path, x=0, y=0, speed=0, move_x=0, move_y=0):
        self.image = pygame.image.load(os.path.join('images', image_path)
            ).convert_alpha()

        self.x = x
        self.y = y

        self.move_speed = speed
        self.move_x = move_x
        self.move_y = move_y

    def update(self, lag_scalar):
        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y), 32, 32), (0, 0, 32, 32))
