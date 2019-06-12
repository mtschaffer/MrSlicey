import os
import math

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
            angle = 180,
            velocity=1.0,
            move_x=0,
            move_y=0
        )

        self.flame_image = pygame.image.load(os.path.join('images', 'flame.png')).convert_alpha()

        self.input_fire_seed = False
        self.move_angle = 0
        self.angle_speed = 2.0
        self.acceleration = 0.5
        self.max_velocity = 10.0

        self.seed_inventory = seed_inventory
        self.seed_fire_cooldown = 200
        self.seed_last_fired = 1000

        self.max_health = 100
        self.health = 100

        self.flame_frame = 0
        self.flame_frame_timer = 0

        self.set_orientation_vector()

    # Read the keystate so we can move
    def input(self, model, keystate):
        self.move_x = 0
        self.move_y = 0
        self.move_angle = 0

        if keystate[pygame.K_LEFT]:
            self.move_angle = self.angle_speed
        elif keystate[pygame.K_RIGHT]:
            self.move_angle = -self.angle_speed

        if keystate[pygame.K_UP]:
            self.velocity += self.acceleration
            if self.velocity > self.max_velocity:
                self.velocity = self.max_velocity
        elif keystate[pygame.K_DOWN]:
            self.velocity -= self.acceleration
            if self.velocity < -self.max_velocity:
                self.velocity = -self.max_velocity

        if keystate[pygame.K_SPACE]:
            self.input_fire_seed = True

    def fire_seed(self, model, seed_velocity):
        if (state.time - self.seed_last_fired > self.seed_fire_cooldown and
                self.seed_inventory > 0):
            self.seed_last_fired = state.time
            self.seed_inventory -= 1

            watermelon_top_x = 10 * self.orientation_vector_x
            watermelon_top_y = 10 * self.orientation_vector_y

            momentum_x = seed_velocity * self.orientation_vector_x
            momentum_y = seed_velocity * self.orientation_vector_y

            seed = Seed(x=self.x + watermelon_top_x, y=self.y + watermelon_top_y,
                momentum_x=momentum_x, momentum_y=momentum_y)
            model.add_fg_element(seed)

            if self.health > 0:
                self.health -= 10

    # Move the watermelon
    def update(self, model, lag_scalar):
        self.angle = self.angle + self.move_angle * lag_scalar

        self.set_orientation_vector()

        self.move_x = self.velocity * self.orientation_vector_x
        self.move_y = self.velocity * self.orientation_vector_y

        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

        if self.input_fire_seed:
            self.input_fire_seed = False
            self.fire_seed(model, self.velocity + 10)

        self.flame_frame_timer += 1
        if self.flame_frame_timer > 1:
            self.flame_frame_timer = 0
            self.flame_frame += 1
            if self.flame_frame > 3:
                self.flame_frame = 0

    def set_orientation_vector(self):
        self.orientation_vector_x = math.sin(math.radians(self.angle))
        self.orientation_vector_y = math.cos(math.radians(self.angle))

    # Draw the watermelon and heath bar and potentialy game over
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle - 180)
        w, h = rotated_image.get_size()

        screen.blit(rotated_image, (int(self.x - w / 2), int(self.y - h / 2)))

        rotated_image = pygame.transform.rotate(self.flame_image.subsurface(self.flame_frame * 20, 0, 20, 20), self.angle - 180)
        w, h = rotated_image.get_size()

        screen.blit(rotated_image, (int(self.x - 23 * self.orientation_vector_x - w / 2),
            int(self.y - 23 * self.orientation_vector_y - h / 2)))

        #health bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))
        if self.health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (10, 10, 100 * self.health / self.max_health, 10))

        #velocity bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 300, 10, 100))
        velocity_bar_height = 100 * abs(self.velocity) / self.max_velocity
        pygame.draw.rect(screen, (0, 255, 0), (10, 400 - velocity_bar_height, 10, velocity_bar_height))

        # TODO: add a new scene for the game over screen
        if self.health <= 0:
            game_over.draw(screen)
