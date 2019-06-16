from scene import state
from utils.sprite import Sprite


class Projectile(Sprite):
    def __init__(self, *args, **kwargs):
        self.momentum_x = kwargs.pop('momentum_x', 0)
        self.momentum_y = kwargs.pop('momentum_y', 0)

        super().__init__(*args, **kwargs)

    def update(self, model, lag_scalar):
        self.x += (self.move_x + self.momentum_x) * lag_scalar
        self.y += (self.move_y + self.momentum_y) * lag_scalar
        radius = self.collider.radius
        if (self.x < -radius
            or self.x > (state.SCREEN_WIDTH + radius)
            or self.y < -radius
            or self.y > (state.SCREEN_HEIGHT + radius)):
            model.remove_fg_element(self)
