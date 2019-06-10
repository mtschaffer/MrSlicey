import pygame


class FGElement(object):
    def __init__(self, image_path, x=0, y=0, speed=0, move_x=0, move_y=0):
        self.image = pygame.image.load(image_path).convert_alpha()

        self.x = x
        self.y = y

        self.move_speed = speed
        self.move_x = move_x
        self.move_y = move_y

    def input(self, model, keystate):
        pass

    def update(self, lag_scalar):
        pass

    def draw(self, screen):
        pass
