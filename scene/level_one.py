from characters.watermelon import Watermelon
from gfx.bg import ParallaxBackground
from scene import state
from utils.text import Text


background = ParallaxBackground((640, 480))
# this set of background images is 272 x 160
# apply hardcoded 4x scale to for now
bg_size = (272 * 4, 160 * 4)
background.add_layer('parallax-mountain-bg.png', 3, 0, bg_size)
background.add_layer('parallax-mountain-montain-far.png', 2, 0, bg_size)
background.add_layer('parallax-mountain-mountains.png', 1.5, 0, bg_size)
background.add_layer('parallax-mountain-trees.png', 1.3, 0, bg_size)
background.add_layer('parallax-mountain-foreground-trees.png', 1.1, 0, bg_size)
watermelon = Watermelon()
hello = Text("Hi, I'm Mr Slicey!", 100, 100)


def draw(screen):
    # Draw the background
    background.draw(screen)

    # Draw text
    if state.time < 5000:
        hello.draw(screen)

    # Draw our player
    watermelon.draw(screen)


def update(lag_scalar):
    # Update the background
    background.update(lag_scalar)

    # Update our player and objects
    watermelon.update(lag_scalar)


def input(keystate):
    # Send the keyboard input so our hero can react
    watermelon.input(keystate)

    # pass queued player movements to the background so it can scroll as the player moves
    background.scroll(watermelon.move_x, watermelon.move_y)
