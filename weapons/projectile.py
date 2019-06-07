import os

import pygame

from utils.fg_element import FGElement

class Projectile(FGElement):
    def update(self, lag_scalar):
        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar
