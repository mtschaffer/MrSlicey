import pygame

from utils.audio import audio
from utils.text import Text
from scene import state, level_one


welcome = Text("GAME OVER", 320, 100, center=True)
subtext = Text("you died", 320, 140, center=True)
restart_instructions = Text("Hit Space to return to the title screen", 320, 360, center=True)
quit_instructions = Text("Or hit Esc to leave :(", 320, 400, center=True)


def enter():
    audio.stop_all()
    audio.play_sfx('ohno')
    pygame.time.wait(3000)
    audio.play_bgm('you_are_dead')


def exit():
    pass


def draw(screen):
    welcome.draw(screen)
    subtext.draw(screen)
    restart_instructions.draw(screen)
    quit_instructions.draw(screen)


def update(lag_scalar):
    pass


def input(keystate, previous_keystate):
    if keystate[pygame.K_SPACE] and (not previous_keystate or not previous_keystate[pygame.K_SPACE]):
        state.fade_to('main_menu')
