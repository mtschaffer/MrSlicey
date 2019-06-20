from itertools import combinations
from random import randint

import pygame

from characters.watermelon import Watermelon
from characters.turkeyleg import TurkeyLeg, IMAGE as TURKEY_IMAGE
from gfx.bg import ParallaxBackground
from scene import state
from utils.collision import collide
from utils.text import Text
from weapons.seed import Seed


class LevelOneModel:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = LevelOneModel()

        return cls._instance

    def __init__(self):
        ## Foreground
        # A list of all on-screen elements.
        self.fg_elements = []
        self.colliders = []
        self.show_colliders = False

        self.add_obstacles()

        self.watermelon = Watermelon(seed_inventory=30)
        self.add_fg_element(self.watermelon)

        self.hello = Text("Hi, I'm Mr Slicey!", 320, 150, center=True)
        self.add_fg_element(self.hello)

        ## Background
        # this set of background images is 272 x 160
        # apply hardcoded 4x scale to for now
        self.bg_size = (272 * 4, 160 * 4)
        self.background = ParallaxBackground((state.SCREEN_WIDTH, state.SCREEN_HEIGHT))
        self.background.add_layer('parallax-mountain-bg.png', 3, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-montain-far.png', 2, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-mountains.png', 1.5, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-trees.png', 1.3, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-foreground-trees.png', 1.1,
            0, self.bg_size)

    def all_fg_elements(self):
        return self.fg_elements

    def add_fg_element(self, value):
        self.fg_elements.append(value)
        if hasattr(value, 'collider'):
            self.colliders.append(value.collider)

    def remove_fg_element(self, element):
        if element in self.fg_elements:
            self.fg_elements.remove(element)
        if hasattr(element, 'collider') and element.collider in self.colliders:
            self.colliders.remove(element.collider)

    def add_obstacles(self):
        w, h = TURKEY_IMAGE.get_size()
        # NOTE: place obstacles in 5x5 grid
        x_step = state.SCREEN_WIDTH // 5
        y_step = state.SCREEN_HEIGHT // 5
        for grid_x in range(0, state.SCREEN_WIDTH, x_step):
            for grid_y in range(0, state.SCREEN_HEIGHT, y_step):
                # NOTE: skip the square the player is spawned in
                if grid_x == 2 * x_step and grid_y == 2 * y_step:
                    continue
                x = grid_x + randint(0, x_step - 1)
                y = grid_y + randint(0, y_step - 1)
                angle = randint(0, 359)
                rot_v = randint(-45, 45)
                self.add_fg_element(TurkeyLeg(x=x, y=y, angle=angle, rotational_velocity=rot_v))


def draw(screen):
    model = LevelOneModel.instance()

    model.background.draw(screen)

    # Draw our elements
    for e in model.all_fg_elements():
        e.draw(screen)


def update(lag_scalar):
    model = LevelOneModel.instance()

    # Update the background
    model.background.update(lag_scalar)

    # Remove hello text
    if state.time > 5000 and model.hello:
        model.remove_fg_element(model.hello)
        model.hello = None

    # Update our player and objects
    for e in model.all_fg_elements():
        e.update(model, lag_scalar)

    for c1, c2 in combinations(model.colliders, 2):
        collide(c1, c2)


def input(keystate, previous_keystate):
    model = LevelOneModel.instance()

    if keystate[pygame.K_c] and (not previous_keystate or not previous_keystate[pygame.K_c]):
        model.show_colliders = not model.show_colliders

    # pass queued player movements to the background so it can scroll as the player moves
    model.background.scroll(model.watermelon.move_x, model.watermelon.move_y)

    # Send the keyboard input so our hero can react
    for e in model.all_fg_elements():
        e.input(model, keystate)
