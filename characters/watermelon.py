import os
import math

import pygame

from camera.camera import camera
from scene import state
from utils.audio import audio
from utils.screen_shake import screen_shake
from utils.sprite import Sprite, Collider
from utils.collision import CollisionEffect
from weapons.seed import Seed

IMAGE_PATH = os.path.join('images', 'watermelon.png')

class Watermelon(Sprite):
    # Load the watermelon image and stick it in the middle of the screen
    def __init__(self, seed_inventory=0):
        super().__init__(
            image=IMAGE_PATH,
            x=320,
            y=240,
            angle=180,
            velocity=1.0,
            move_x=0,
            move_y=0
        )

        self.flame_image = pygame.image.load(os.path.join('images', 'flame.png')).convert_alpha()

        self.input_fire_seed = False
        self.move_angle = 0

        self.rotation_speed = 2.0
        self.acceleration = 0.5
        self.max_velocity = 10.0
        self.move_velocity = 0

        self.seed_inventory = seed_inventory
        self.seed_fire_cooldown = 200
        self.seed_last_fired = 1000

        self.max_health = 100
        self.health = 100

        self.flame_frame = 0
        self.flame_frame_timer = 0

        self.set_orientation_vector()

    def create_collider(self):
        return Collider(self, reaction=self.collided)

    def collided(self, collider, effect):
        if effect == CollisionEffect.Halt:
            self.acceleration = self.move_velocity = self.velocity = self.health = 0
            collider.collided = True

    # Read the keystate so we can move
    def input(self, model, keystate):
        self.reset_buffered_input()

        if keystate[pygame.K_LEFT]:
            self.move_angle = self.rotation_speed
        elif keystate[pygame.K_RIGHT]:
            self.move_angle = -self.rotation_speed

        if keystate[pygame.K_UP]:
            self.move_velocity = self.acceleration
        elif keystate[pygame.K_DOWN]:
            self.move_velocity = -self.acceleration

        if keystate[pygame.K_SPACE]:
            audio.play_sfx('pew')
            self.input_fire_seed = True

    def reset_buffered_input(self):
        self.move_x = 0
        self.move_y = 0
        self.move_angle = 0
        self.move_velocity = 0
        self.input_fire_seed = False

    def fire_seed(self, model, seed_velocity):
        if (state.time - self.seed_last_fired > self.seed_fire_cooldown and
                self.seed_inventory > 0):
            self.seed_last_fired = state.time
            self.seed_inventory -= 1

            watermelon_top_x = 10 * self.orientation_vector_x
            watermelon_top_y = 10 * self.orientation_vector_y

            momentum_x = seed_velocity * self.orientation_vector_x
            momentum_y = seed_velocity * self.orientation_vector_y

            seed = Seed(self, x=self.x + watermelon_top_x, y=self.y + watermelon_top_y,
                momentum_x=momentum_x, momentum_y=momentum_y)
            model.add_fg_element(seed)

            if self.health > 0:
                self.health -= 10

    def projectile_hit(self):
        self.health = min(self.health + 15, self.max_health)

    # Move the watermelon
    def update(self, model, lag_scalar):
        super().update(model, lag_scalar)
        self.angle = self.angle + self.move_angle * lag_scalar
        self.angle %= 360
        self.set_orientation_vector()

        self.velocity = max(min(self.max_velocity, self.velocity + self.move_velocity), -self.max_velocity)

        self.move_x = self.velocity * self.orientation_vector_x
        self.move_y = self.velocity * self.orientation_vector_y

        self.x = self.x + self.move_x * lag_scalar
        self.y = self.y + self.move_y * lag_scalar

        if self.input_fire_seed:
            self.fire_seed(model, max(-2, self.velocity) + 10)
            state.offset = screen_shake(2, 3)
            state.screen_shaking = True

        self.animate_flame()

        if self.velocity > 0:
            audio.stop_infinite_sfx('beepbeepbeep')
            audio.play_infinite_sfx('rocket', volume=(abs(self.velocity) / self.max_velocity))
        elif self.velocity < 0:
            audio.stop_infinite_sfx('rocket')
            audio.play_infinite_sfx('beepbeepbeep', volume=(abs(self.velocity) / self.max_velocity))
        else:
            audio.stop_infinite_sfx('rocket')
            audio.stop_infinite_sfx('beepbeepbeep')

        if (self.health / self.max_health) < .25:
            audio.play_infinite_sfx('heartbeat')
        else:
            audio.stop_infinite_sfx('heartbeat')


    def animate_flame(self):
        velocity_based_animation_rate = 2 - int(abs(self.velocity) / 4)
        self.flame_frame_timer += 1
        if self.flame_frame_timer > velocity_based_animation_rate:
            self.flame_frame_timer = 0
            self.flame_frame += 1
            if self.flame_frame > 3:
                self.flame_frame = 0

    def set_orientation_vector(self):
        self.orientation_vector_x = math.sin(math.radians(self.angle))
        self.orientation_vector_y = math.cos(math.radians(self.angle))

    # Draw the watermelon and heath bar and potentialy game over
    def draw(self, screen):
        super().draw(screen)
        self.draw_player(screen)
        self.draw_flame(screen)

        # TODO: Move these displays to a HUD class
        self.draw_hud(screen)

        if self.health <= 0:
            state.fade_to('game_over')

    def draw_player(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle - 180)
        w, h = rotated_image.get_size()
        camera.blit(rotated_image, (self.x - w / 2, self.y - h / 2))

    def draw_flame(self, screen):
        image_height = int(abs(self.velocity)) + 10
        flame_subsurface = self.flame_image.subsurface(self.flame_frame * 20, 20 - image_height, 20, image_height)
        rotated_image = pygame.transform.rotate(flame_subsurface, self.angle - 180)
        w, h = rotated_image.get_size()

        distance_from_center = (20 + int(abs(self.velocity) / 2))
        camera.blit(rotated_image, (self.x - distance_from_center * self.orientation_vector_x - w / 2,
            self.y - distance_from_center * self.orientation_vector_y - h / 2))

    def draw_hud(self, screen):
        # health bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))
        if self.health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (10, 10, 100 * self.health / self.max_health, 10))

        # velocity bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 370, 10, 100))
        bar_height = 100 * abs(self.velocity) / self.max_velocity
        if bar_height > 0:
            color = (0, 255, 0) if self.velocity > 0 else (255, 192, 0)
            pygame.draw.rect(screen, color, (10, 470 - bar_height, 10, bar_height))
