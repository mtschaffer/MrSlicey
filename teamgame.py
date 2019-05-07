import pygame
from scene import state

#Rules:
#1) Worked on in your free time
#2) Can't remove other contributors' features
#3) You can add a single feature on your turn
#4) Feature must make the game "more fun"
WHITE = (0xFF, 0xFF, 0xFF)

def main():
    pygame.init()

    pygame.display.set_caption("The Wonderful Watermelon World of Mr Slicey: Quest for the Rest of the Melon")

    #Game clock used for framerate calculations
    clock = pygame.time.Clock()

    #VGA resolution sounds about right
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Let's aim for 30 frames/second
    fps = 30

    #Ideally at 30 fps, each frame should take 33.3ms however this is not guarenteed
    #This scalar is updated every loop to help scale movement to allow smooth movement
    #when the time between frames is not always consistent
    lag_scalar = 1.0

    state.load_scene('main_menu')

    while (True):
        state.loop(lag_scalar, screen)

        msElapsed = clock.tick(fps)
        lag_scalar = msElapsed * fps / 1000.0


main()
