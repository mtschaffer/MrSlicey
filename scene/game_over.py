import pygame

from utils.audio import audio
from utils.text import Text
from scene import state, level_one


welcome = Text("GAME OVER", 320, 100, center=True)
subtext = Text("you died", 320, 140, center=True)
restart_instructions = Text("Hit Space to return to the title screen", 320, 360, center=True)
quit_instructions = Text("Or hit Esc to leave :(", 320, 400, center=True)
score_text = None
time_text = None


def enter(scene_args):
    global score_text
    global time_text

    audio.stop_all()
    audio.play_sfx('ohno')
    audio.play_bgm('you_are_dead')

    score_text = Text("Score: {}".format(scene_args["score"]), 200, 200, center=True)
    time_text = Text("Time: {}".format(round(scene_args["time"], 3)), 440, 200, center=True)


def exit():
    pass


def draw(screen):
    welcome.draw(screen)
    subtext.draw(screen)
    score_text.draw(screen)
    time_text.draw(screen)
    restart_instructions.draw(screen)
    quit_instructions.draw(screen)


def update(lag_scalar):
    pass


def input(keystate, previous_keystate):
    #if keystate[pygame.K_SPACE] and (not previous_keystate or not previous_keystate[pygame.K_SPACE]):
    #    state.fade_to('main_menu', None)
    pass
