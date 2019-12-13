"""
Manage different scenes for the game.
"""
import sys
from importlib import import_module

import pygame

from utils.screen_shake import screen_shake


def _quit(keystate):
    alt_held = keystate[pygame.K_LALT] or keystate[pygame.K_RALT]
    ctrl_held = keystate[pygame.K_LCTRL] or keystate[pygame.K_RCTRL]

    # Read some key events to see if we need to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and ctrl_held:
                return True
            if event.key == pygame.K_F4 and alt_held:
                return True
            if event.key == pygame.K_ESCAPE:
                return True

    return False


class SceneState:
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    def __init__(self):
        self.current_scene = None
        self.next_scene = None
        self._scene_cache = {}
        self._scene_time_stamp = 0
        self.offset = screen_shake(0,0)
        self.previous_keystate = None
        self.screen_shaking = False

        self.alphaSurface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.alphaSurface.fill((0,0,0))
        self.alphaSurface.set_alpha(0)
        self.alpha = 0

    def load_scene(self, scene_name, scene_args):
        if scene_name not in self._scene_cache:
            scene = import_module('scene.{}'.format(scene_name))
            self._scene_cache[scene_name] = scene

        if self.current_scene:
            self.current_scene.exit()

        self.current_scene = self._scene_cache[scene_name]
        self._scene_time_stamp = pygame.time.get_ticks()

        self.current_scene.enter(scene_args)

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    def fade_to(self, scene, scene_args):
        self.next_scene = scene
        self.next_scene_args = scene_args
        self.alpha = 0

    @property
    def time(self):
        """
        Get elapsed time from scene load.
        :return: time (ms)
        """
        return pygame.time.get_ticks() - self._scene_time_stamp

    def loop(self, lag_scalar, screen):
        # Get the complete keyboard state
        keystate = pygame.key.get_pressed()
        current_scene = self.current_scene

        if _quit(keystate):
            pygame.quit()
            sys.exit()

        # Handle ongoing input even when there are no events
        current_scene.input(keystate, self.previous_keystate)
        current_scene.update(lag_scalar)
        self.previous_keystate = keystate

        # Start drawing this frame by painting the whole thing black
        screen.fill((0, 0, 0))
        current_scene.draw(screen)

        if self.screen_shaking:
            screen_copy = screen.copy()
            shake = next(self.offset)
            screen.blit(screen_copy, shake)
            if shake is (0, 0):
                self.screen_shaking = False

        if self.next_scene:
            print(self.alpha)
            if self.alpha < 255:
                self.alpha += 8.0
                self.alphaSurface.set_alpha(self.alpha)
                screen.blit(self.alphaSurface, (0,0))
                screen.set_alpha(self.alpha)
            else:
                screen.fill((0,0,0))
                self.load_scene(self.next_scene, self.next_scene_args)
                self.next_scene = None

        pygame.display.flip()


state = SceneState()
