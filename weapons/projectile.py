import weakref

from utils.collision import CollisionEffect
from utils.sprite import Sprite, Collider


class Projectile(Sprite):
    def __init__(self, owner, *args, **kwargs):
        self.momentum_x = kwargs.pop('momentum_x', 0)
        self.momentum_y = kwargs.pop('momentum_y', 0)
        self.owner = weakref.ref(owner)
        self.impacted = False

        super().__init__(*args, **kwargs)

    def create_collider(self):
        return Collider(self, effect=CollisionEffect.Destroy, reaction=self.collided)

    def collided(self, collider, effect):
        if effect == CollisionEffect.Halt:
            self.owner().projectile_hit()
            self.impacted = True

    def update(self, model, lag_scalar):
        super().update(model, lag_scalar)
        self.x += (self.move_x + self.momentum_x) * lag_scalar
        self.y += (self.move_y + self.momentum_y) * lag_scalar
        radius = self.collider.radius
        if self.impacted:  # TODO remove projectile if it travels outside level
            model.remove_fg_element(self)
