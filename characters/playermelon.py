import math

import pygame

from camera.camera import camera
from characters.watermelon import Watermelon
from scene import state
from utils.audio import audio
from utils.collision import CollisionEffect
from utils.screen_shake import screen_shake
from utils.sprite import Collider
from weapons.seed import Seed


class PlayerMelon(Watermelon):
    # Load the watermelon image and stick it in the middle of the screen
    def __init__(self, seed_inventory=0, x=320, y=240, velocity=1.0):
        super().__init__(
            x=x,
            y=y,
            velocity=velocity,
            seed_inventory=seed_inventory
        )

        self._lifesteal = 15

        self.input_fire_seed = False
        self.input_fire_behind = False
        self.input_fire_fan = False

        self.move_angle = 0

        self.rotation_speed = 3.0
        self.acceleration = 0.5
        self.max_velocity = 10.0
        self.move_velocity = 0

        self.seed_inventory = seed_inventory
        self.seed_fire_cooldown = 200
        self.seed_last_fired = 0

        self.max_health = 100
        self.health = 100

        self.flame_frame = 0
        self.flame_frame_timer = 0

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

        if keystate[pygame.K_z]:
            audio.play_sfx('pew')
            self.input_fire_behind = True
        elif keystate[pygame.K_x]:
            audio.play_sfx('pew')
            self.input_fire_fan = True
        elif keystate[pygame.K_SPACE]:
            audio.play_sfx('pew')
            self.input_fire_seed = True

    def reset_buffered_input(self):
        self.move_x = 0
        self.move_y = 0
        self.move_angle = 0
        self.move_velocity = 0
        self.input_fire_seed = False
        self.input_fire_behind = False
        self.input_fire_fan = False

    def fire(self, model, seed_velocity):
        self.fire_seed(model, seed_velocity)
        self.seed_last_fired = state.time

    def fire_behind(self, model, seed_velocity):
        self.fire_seed(model, seed_velocity, angle=180)
        self.seed_last_fired = state.time

    def fire_fan(self, model, seed_velocity):
        fan_spread = 40
        self.fire_seed(model, seed_velocity, angle=-fan_spread)
        self.fire_seed(model, seed_velocity, angle=0)
        self.fire_seed(model, seed_velocity, angle=fan_spread)
        self.seed_last_fired = state.time

    def can_fire(self, num_shots):
        return state.time - self.seed_last_fired > self.seed_fire_cooldown and \
               self.seed_inventory > num_shots

    def fire_seed(self, model, seed_velocity, angle=0, num_shots=1):
        if self.can_fire(num_shots):
            self.seed_inventory -= 1

            watermelon_top_x = 10 * self.orientation_vector_x
            watermelon_top_y = 10 * self.orientation_vector_y

            abs_angle = self.angle + angle
            nx = math.sin(math.radians(abs_angle))
            ny = math.cos(math.radians(abs_angle))

            if angle == 180:
                # adjust for no momentum since we're relying on vector sums
                # we'd have a projectile with no momentum  (a * 0 = 0)
                momentum_x = seed_velocity * -self.orientation_vector_x
                momentum_y = seed_velocity * -self.orientation_vector_y
            else:
                momentum_x = seed_velocity * (self.orientation_vector_x + nx)
                momentum_y = seed_velocity * (self.orientation_vector_y + ny)

            seed = Seed(self, x=self.x + watermelon_top_x, y=self.y + watermelon_top_y,
                        angle=abs_angle,
                        momentum_x=momentum_x, momentum_y=momentum_y)
            model.add_fg_element(seed)

            if self.health > 0:
                self.health -= 10

            state.offset = screen_shake(2, 3)
            state.screen_shaking = True

    def projectile_hit(self):
        self.health = min(self.health + self._lifesteal, self.max_health)

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
            self.fire(model, max(-2, self.velocity) + 10)
            self.seed_last_fired = state.time

        if self.input_fire_behind:
            self.fire_behind(model, max(-2, self.velocity) + 10)
            self.seed_last_fired = state.time

        if self.input_fire_fan:
            if self.seed_inventory > 3:
                self.fire_fan(model, max(-2, self.velocity) + 10)
                self.seed_last_fired = state.time

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

    # Draw the watermelon and heath bar and potentialy game over
    def draw(self, screen):
        super().draw(screen)
        self.draw_melon(screen)
        self.draw_flame(screen)

        # TODO: Move these displays to a HUD class
        self.draw_hud(screen)

    def create_collider(self):
        return Collider(self, effect=CollisionEffect.Player, reaction=self.collided)

    def collided(self, collider, effect):
        super().collided(collider, effect)

        if effect == CollisionEffect.Halt:
            self.acceleration = self.move_velocity = self.velocity = self.health = 0
            collider.collided = True
