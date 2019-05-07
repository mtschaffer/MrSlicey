from characters.watermelon import Watermelon
from scene import state
from utils.text import Text

watermelon = Watermelon()
hello = Text("Hi, I'm Mr Slicey!", 100, 100)

def draw(screen):
    # Draw text
    if state.time < 5000:
        hello.draw(screen)

    # Draw our player
    watermelon.draw(screen)


def update(lag_scalar):
    # Update our player and objects
    watermelon.update(lag_scalar)


def input(keystate):
    # Send the keyboard input so our hero can react
    watermelon.input(keystate)
