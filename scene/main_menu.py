import pygame

from utils.text import Text
from scene import state


welcome = Text("THE WONDERFUL WATERMELON WORLD OF MR SLICEY", 320, 100, center=True)
subtext = Text("...quest for the rest of the melon", 320, 140, center=True)
next_text = Text("Hit Space to Enter the Wonderful World!", 320, 400, center=True)

controls1_text = Text("Left/Right Arrows - Rotate", 50, 230)
controls2_text = Text("Up/Down Arrows - Speed", 50, 260)
controls3_text = Text("Spacebar - Shoot", 50, 290)


def draw(screen):
    welcome.draw(screen)
    subtext.draw(screen)
    next_text.draw(screen)

    controls1_text.draw(screen)
    controls2_text.draw(screen)
    controls3_text.draw(screen)


def update(lag_scalar):
    pass


def input(keystate, event=None):
    if keystate[pygame.K_SPACE]:
        state.load_scene('level_one')
