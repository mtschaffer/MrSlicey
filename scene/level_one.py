from characters.watermelon import Watermelon
from gfx.bg import ParallaxBackground
from scene import state
from utils.text import Text


class LevelOneModel:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = LevelOneModel()

        return cls._instance

    def __init__(self):
        ## Foreground
        # A dict of all on-screen elements
        self._fg_elements = {}

        self.watermelon = Watermelon()
        self.add_fg_element('watermelon', self.watermelon)

        self.hello = Text("Hi, I'm Mr Slicey!", 100, 100)
        self.add_fg_element('hello', self.hello)

        ## Background
        # this set of background images is 272 x 160
        # apply hardcoded 4x scale to for now
        self.bg_size = (272 * 4, 160 * 4)
        self.background = ParallaxBackground((640, 480))
        self.background.add_layer('parallax-mountain-bg.png', 3, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-montain-far.png', 2, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-mountains.png', 1.5, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-trees.png', 1.3, 0,
            self.bg_size)
        self.background.add_layer('parallax-mountain-foreground-trees.png', 1.1,
            0, self.bg_size)

    def all_fg_elements(self):
        return self._fg_elements.values()

    def add_fg_element(self, name, value):
        self._fg_elements[name] = value

    def remove_fg_element(self, name):
        element = self._fg_elements.get(name)
        if name in self._fg_elements:
            del self._fg_elements[name]


def draw(screen):
    model = LevelOneModel.instance()

    # Remove Text after such time
    if state.time > 5000:
        model.remove_fg_element('hello')

    model.background.draw(screen)

    # Draw our elements
    for e in model.all_fg_elements():
        e.draw(screen)


def update(lag_scalar):
    model = LevelOneModel.instance()

    # Update the background
    model.background.update(lag_scalar)

    # Update our player and objects
    for e in model.all_fg_elements():
        e.update(lag_scalar)


def input(keystate):
    model = LevelOneModel.instance()

    # pass queued player movements to the background so it can scroll as the player moves
    model.background.scroll(model.watermelon.move_x, model.watermelon.move_y)

    # Send the keyboard input so our hero can react
    for e in model.all_fg_elements():
        e.input(keystate)
