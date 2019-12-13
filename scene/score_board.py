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
        self.seed_count = 0

    def incr_score(self, amount):
        self.score += amount
        print(self.score)

    def update_seed_count(self, count):
        self.seed_count = count

    def draw(self, screen):
        score_text = Text(str(self.score), state.SCREEN_WIDTH / 2, 0, center=True)
        score_text.draw(screen)

        seed_text = Text(f'seeds: {self.seed_count}', 10, 25)
        seed_text.draw(screen)

    def input(self, model, keystate):
        return

    def update(self, model, lag_scalar):
        return
