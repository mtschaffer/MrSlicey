import enum
import math


def collide(collider1, collider2):
    one_x, one_y = collider1.center
    two_x, two_y = collider2.center
    a = one_x - two_x
    b = one_y - two_y
    distance = math.sqrt((a ** 2) + (b ** 2))
    if distance < (collider1.radius + collider2.radius):
        handle_collision(collider1, collider2)


def handle_collision(collider1, collider2):
    collider1.react(collider2.effect)
    collider2.react(collider1.effect)


class CollisionEffect(enum.Enum):
    Nothing = enum.auto()
    Halt = enum.auto()
    Destroy = enum.auto()


def null_reaction(collider, effect):
    pass
