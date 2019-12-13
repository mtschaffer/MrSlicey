import pygame

from utils.audio import audio
from utils.text import Text
from scene import state


welcome = Text("THE WONDERFUL WATERMELON WORLD OF MR SLICEY", 320, 100, center=True)
subtext = Text("...quest for the rest of the melon", 320, 140, center=True)
next_text = Text("Hit Space to Enter the Wonderful World!", 320, 400, center=True)

controls1_text = Text("Left/Right Arrows - Rotate", 50, 230)
controls2_text = Text("Up/Down Arrows - Speed", 50, 260)
controls3_text = Text("Spacebar - Shoot", 50, 290)
controls4_text = Text("(Debug): c - Toggle visible hitboxes", 50, 320)


def enter(scene_args):
    audio.stop_all()
    audio.play_bgm('titlescreenfull')


def exit():
    pass


def draw(screen):
    welcome.draw(screen)
    subtext.draw(screen)
    next_text.draw(screen)

    controls1_text.draw(screen)
    controls2_text.draw(screen)
    controls3_text.draw(screen)
    controls4_text.draw(screen)


def update(lag_scalar):
    pass


def input(keystate, previous_keystate):
    if keystate[pygame.K_SPACE] and (not previous_keystate or not previous_keystate[pygame.K_SPACE]):
        state.fade_to('level_one', None)
