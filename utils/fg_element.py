class FGElement(object):
    def __init__(self, x=0, y=0, angle=0, velocity=0, move_x=0, move_y=0):
        self.x = x
        self.y = y

        self.angle = angle
        self.velocity = velocity
        self.move_x = move_x
        self.move_y = move_y


    def input(self, model, keystate):
        pass

    def update(self, model, lag_scalar):
        pass

    def draw(self, screen):
        pass
