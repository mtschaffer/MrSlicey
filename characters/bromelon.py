from characters.watermelon import Watermelon
from utils.collision import CollisionEffect
from utils.sprite import Collider


class BroMelon(Watermelon):

    def __init__(self, x=320, y=240, velocity=1.0):
        super().__init__(
            x=x,
            y=y,
            velocity=velocity
        )
        self.destroyed = False

    def update(self, model, lag_scalar):
        super().update(model, lag_scalar)
        if self.destroyed:
            model.remove_fg_element(self)

    def create_collider(self):
        return Collider(self, reaction=self.collided)

    def collided(self, collider, effect):
        super().collided(collider, effect)

        if effect == CollisionEffect.Player:
            self.apply_powerup()
            collider.collided = True
            self.destroyed = True

        elif effect == CollisionEffect.Halt:
            pass

    def apply_powerup(self):
        self.score_board.incr_score(20)
