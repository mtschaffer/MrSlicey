from itertools import combinations
from random import randint

import pygame

from .score_board import ScoreBoard
from .time_board import TimeBoard
from camera.camera import camera
from characters.bromelon import BroMelon
from characters.playermelon import PlayerMelon
from characters.turkeyleg import TurkeyLeg, IMAGE as TURKEY_IMAGE
from gfx.bg import ParallaxBackground
from scene import state
from utils.audio import audio
from utils.collision import collide
from utils.text import Text


class LevelOneModel:
    _instance = None

    NUM_BROS = 4

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = LevelOneModel()

        return cls._instance

    @classmethod
    def clear_instance(cls):
        cls._instance = None

    def __init__(self):
        ## Foreground
        # A list of all on-screen elements.
        self.fg_elements = []
        self.colliders = []
        self.show_colliders = False

        self.placed_bros = []

        self.populate_grid()

        self.watermelon = PlayerMelon(seed_inventory=30)
        self.add_fg_element(self.watermelon)
        camera.set_target(self.watermelon)

        self.hello = Text("Hi, I'm Mr Slicey!", 320, 150, center=True)
        self.add_fg_element(self.hello)

        self.score_board = ScoreBoard.instance()
        self.add_fg_element(self.score_board)

        self.time_board = TimeBoard.instance()
        self.add_fg_element(self.time_board)

        self.game_over = False

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


    def populate_grid(self):
        w, h = TURKEY_IMAGE.get_size()

        turkey_idx = 0
        # NOTE: place obstacles in 5x5 grid
        x_step = state.SCREEN_WIDTH // 5
        y_step = state.SCREEN_HEIGHT // 5

        center = (2 * x_step, 2 * y_step)
        for grid_x in range(-state.SCREEN_WIDTH, state.SCREEN_WIDTH, x_step):
            for grid_y in range(-state.SCREEN_HEIGHT, state.SCREEN_HEIGHT, y_step):
                # NOTE: skip the square the player is spawned in
                # let the watermelon breathe before the madness
                if abs(center[0] - grid_x) <= x_step and abs(center[1] - grid_y) <= y_step:
                    continue

                x = grid_x + randint(0, x_step - 1)
                y = grid_y + randint(0, y_step - 1)

                # bros are in the 4 corners
                if ((grid_x < -state.SCREEN_WIDTH + x_step) or (grid_x >= state.SCREEN_WIDTH - x_step)) and \
                   ((grid_y < -state.SCREEN_HEIGHT + y_step) or (grid_y >= state.SCREEN_HEIGHT - y_step)):
                    self.add_fg_element(BroMelon(x=x, y=y))


                angle = randint(0, 359)
                rot_v = randint(-45, 45)
                self.add_fg_element(TurkeyLeg(x=x, y=y, angle=angle, rotational_velocity=rot_v, idx=turkey_idx))
                turkey_idx += 1
        print("Turkey Count: " + str(turkey_idx))


def enter(scene_args):
    audio.stop_all()
    audio.play_bgm('bgm1')
    audio.play_sfx('yolo')

    model = LevelOneModel.instance()
    model.time_board.start()

def exit():
    LevelOneModel.clear_instance()


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

    score = model.score_board.instance().score
    time = model.time_board.instance().elapsed_time
<<<<<<< Updated upstream
    if (model.watermelon.health <= 0 or score >= 23) and not model.game_over:
=======
    if model.watermelon.health <= 0 and not model.game_over:
>>>>>>> Stashed changes
        model.game_over = True
        state.fade_to('game_over', {"score": score, "time": time})


def input(keystate, previous_keystate):
    model = LevelOneModel.instance()

    if keystate[pygame.K_c] and (not previous_keystate or not previous_keystate[pygame.K_c]):
        model.show_colliders = not model.show_colliders

    # pass queued player movements to the background so it can scroll as the player moves
    model.background.scroll(model.watermelon.move_x, model.watermelon.move_y)

    # Send the keyboard input so our hero can react
    for e in model.all_fg_elements():
        e.input(model, keystate)
