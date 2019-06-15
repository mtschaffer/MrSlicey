from utils.sprite import Sprite


class Projectile(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.momentum_x = kwargs.pop('momentum_x', 0)
        self.momentum_y = kwargs.pop('momentum_y', 0)

    def update(self, model, lag_scalar):
        self.x = self.x + (self.move_x + self.momentum_x) * lag_scalar
        self.y = self.y + (self.move_y + self.momentum_y) * lag_scalar
