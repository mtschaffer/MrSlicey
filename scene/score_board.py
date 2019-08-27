from scene import state
from utils.text import Text

class ScoreBoard:
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = ScoreBoard()

        return cls._instance

    def __init__(self):
        self.score = 0

    def incr_score(self, amount):
        self.score += amount
        print(self.score)

    def draw(self, screen):
        text = Text(str(self.score), state.SCREEN_WIDTH / 2, 0, center=True)
        text.draw(screen)

    def input(self, model, keystate):
        return

    def update(self, model, lag_scalar):
        return
