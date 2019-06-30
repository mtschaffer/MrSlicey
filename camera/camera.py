class Camera():
    def __init__(self):
        self._target = None
        self._screen = None
        self._x0 = 0
        self._y0 = 0
        
    def set_screen(self, screen):
        self._screen = screen
        
    def set_target(self, target):
        self._target = target
        self._x0 = target.x
        self._y0 = target.y

    def blit(self, source, dest, area=None, special_flags=0):
        if self._screen:
            offset_x = dest[0] - (self._target.x-self._x0) if self._target else dest[0]
            offset_y = dest[1] - (self._target.y-self._y0) if self._target else dest[1]
            offset_dest = (offset_x, offset_y)
            # TODO: Culling: only blit image if on screen, either here or in sprite class which calls this method
            self._screen.blit(source, offset_dest, area, special_flags)


camera = Camera()
