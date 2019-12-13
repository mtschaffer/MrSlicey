from scene import state
from utils.text import Text
import time

class TimeBoard:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = TimeBoard()

        return cls._instance

    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def set_elapsed_time(self):
        self.elapsed_time = time.time() - self.start_time

    def draw(self, screen):
        self.set_elapsed_time()
        text = Text(str(round(self.elapsed_time, 3)), state.SCREEN_WIDTH - 40, 460, center=True)
        text.draw(screen)

    def input(self, model, keystate):
        return

    def update(self, model, lag_scalar):
        return
