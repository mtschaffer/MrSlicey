import os

import pygame

IMAGE_PATH = os.path.join('images', 'watermelon.png')


class Watermelon:

    # Load the watermelon image and stick it in the middle of the screen
    def __init__(self):
        self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        self.x = 320
        self.y = 240

        self.move_speed = 4.0
        self.move_x = 0
        self.move_y = 0

    # Read the keystate so we can move
    def input(self, keystate):
        self.move_x = 0
        if keystate[pygame.K_LEFT]:
            self.move_x = -self.move_speed
        elif keystate[pygame.K_RIGHT]:
            self.move_x = self.move_speed

        self.move_y = 0
        if keystate[pygame.K_UP]:
            self.move_y = -self.move_speed
        elif keystate[pygame.K_DOWN]:
            self.move_y = self.move_speed

    # Move the watermelon
    def update(self, lag_scalar):
        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

    # Draw the watermelon
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y), 32, 32), (0, 0, 32, 32))
