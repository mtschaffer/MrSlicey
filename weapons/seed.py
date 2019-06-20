import os
from random import randint

import pygame

from .projectile import Projectile


IMAGE_PATH_BASE = os.path.join('images', 'seeds')


class Seed(Projectile):
    def __init__(self, *args, **kwargs):
        num = randint(1, 5)
        image_path = IMAGE_PATH_BASE + '/seed{}.png'.format(num)

        super().__init__(*args, image=image_path, **kwargs)

        self.image = pygame.transform.scale(self.image, (10, 10))
        self.collider.update_size()

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, (int(self.x - 5), int(self.y - 5), 10, 10), (0, 0, 10, 10))
