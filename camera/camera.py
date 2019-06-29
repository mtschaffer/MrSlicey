class Camera:
    def __init__(self, target, fg_elements):
        self.target = target
        self.fg_elements = fg_elements
        self.x0 = target.x
        self.y0 = target.y
        self.dx = 0
        self.dy = 0
        
    def _calculate_offset(self):
        self.dx = self.target.x - self.x0
        self.dy = self.target.y - self.y0
    
    def _center_target(self):
        self.target.x = self.x0
        self.target.y = self.y0
        
    def _update_fg_positions(self):
        for fg in self.fg_elements:
            fg.x -= self.dx
            fg.y -= self.dy

    def update(self):
        self._calculate_offset()
        self._update_fg_positions()
        self._center_target()
