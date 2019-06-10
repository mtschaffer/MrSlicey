import os

import pygame

from utils.fg_element import FGElement

class Projectile(FGElement):
    def __init__(self, *args, **kwargs):
        self.momentum_x = kwargs.pop('momentum_x', 0)
        self.momentum_y = kwargs.pop('momentum_y', 0)

        super().__init__(*args, **kwargs)

    def update(self, lag_scalar):
        self.x = self.x + (self.move_x + self.momentum_x) * lag_scalar
        self.y = self.y + (self.move_y + self.momentum_y) * lag_scalar
