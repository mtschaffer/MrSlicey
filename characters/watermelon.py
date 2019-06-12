import os

import pygame

from utils.text import Text
from scene import state
from utils.fg_element import FGElement
from weapons.seed import Seed

IMAGE_PATH = os.path.join('images', 'watermelon.png')

game_over = Text("GAME OVER", 250, 200)

class Watermelon(FGElement):
    # Load the watermelon image and stick it in the middle of the screen
    def __init__(self, seed_inventory=0):
        super().__init__(
            image_path=IMAGE_PATH,
            x=320,
            y=240,
            speed=4.0,
            move_x=0,
            move_y=0
        )

        self.seed_inventory = seed_inventory
        self.seed_fire_cooldown = 200
        self.seed_last_fired = 1000
        self.health = 100
        self.health_display = 0

    # Read the keystate so we can move
    def input(self, model, keystate):
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

        if keystate[pygame.K_SPACE]:
            self.fire_seed(model)

    def fire_seed(self, model):
        if (state.time - self.seed_last_fired > self.seed_fire_cooldown and
                self.seed_inventory > 0):
            self.seed_last_fired = state.time
            self.seed_inventory -= 1

            # TODO: we could set momentum based on watermelon orientation
            # TODO: set the x cooridinate based on self.x + self.width / 2
            seed = Seed(x=self.x + 10, y=self.y, momentum_y=-10)
            model.add_fg_element(seed)
            if self.health > 0:
                self.health -= 10
                self.health_display += 10

    # Move the watermelon
    def update(self, lag_scalar):
        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

    # Draw the watermelon and heath bar and potentialy game over
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y), 32, 32), (0, 0, 32, 32))
        pygame.draw.rect(screen, (255,0,0), (10, 10, 100, 10))
        pygame.draw.rect(screen, (0,255,0), (10, 10,  100 - self.health_display, 10))
        if self.health <= 0:
            game_over.draw(screen)
