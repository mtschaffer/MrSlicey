import pygame

from utils.text import Text
from scene import state


welcome = Text("THE WONDERFUL WATERMELON WORLD OF MR SLICEY", 0, 100)
subtext = Text("...quest for the rest of the melon", 0, 150)
next_text = Text("Hit Space to Enter the Wonderful World!", 200, 300)


def draw(screen, tick):
    welcome.draw(screen)
    subtext.draw(screen)
    next_text.draw(screen)


def update(lag_scalar):
    pass


def input(keystate):
    if keystate[pygame.K_SPACE]:
        state.load_scene('level_one')

