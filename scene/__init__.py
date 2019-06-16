"""
Manage different scenes for the game.
"""
import sys
from importlib import import_module

import pygame


def _quit(keystate, event):
    alt_held = keystate[pygame.K_LALT] or keystate[pygame.K_RALT]
    ctrl_held = keystate[pygame.K_LCTRL] or keystate[pygame.K_RCTRL]

    # Read some key events to see if we need to quit
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
        self._scene_cache = {}
        self._scene_time_stamp = 0

    def load_scene(self, scene_name):
        if scene_name not in self._scene_cache:
            scene = import_module('scene.{}'.format(scene_name))
            self._scene_cache[scene_name] = scene

        self.current_scene = self._scene_cache[scene_name]
        self._scene_time_stamp = pygame.time.get_ticks()

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

        for event in pygame.event.get():
            if _quit(keystate, event):
                pygame.quit()
                sys.exit()
            current_scene.input(keystate, event)

        # Handle ongoing input even when there are no events
        current_scene.input(keystate)
        current_scene.update(lag_scalar)

        # Start drawing this frame by painting the whole thing black
        screen.fill((0, 0, 0))
        current_scene.draw(screen)
        pygame.display.flip()


state = SceneState()
