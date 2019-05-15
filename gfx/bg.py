import os

import pygame


class ParallaxLayer:

    def __init__(self, surface, factor_x, factor_y):
        self.surface = surface
        self.factor_x = factor_x
        self.factor_y = factor_y
        self.posx = 0
        self.posy = 160

    def scroll(self, scroll_x, scroll_y):
        if self.factor_x:
            self.posx += (scroll_x / self.factor_x)
            self.posx %= self.surface.get_width()
        if self.factor_y:
            self.posy += scroll_y / self.factor_y


class ParallaxBackground:

    # blit a sequence of images onto the background
    # scroll each layer at a different rate
    def __init__(self, size=None):
        self.layers = []
        self.size = size
        self._queued_scroll_x = 0
        self._queued_scroll_y = 0

    def draw(self, screen):
        if not self.layers:
            return
        sw, sh = self.size
        # blit each background layer onto the screen in order from back to front
        for layer in self.layers:
            screen.blit(layer.surface, (0, 0), (layer.posx, layer.posy, sw, sh))
            # tile the layer horizontally if its factor_x is nonzero
            # tile the layer vertically if its factor_y is nonzero
            # this makes the modulus positioning used in ParallaxLayer.scroll seamless
            lw, lh = layer.surface.get_width(), layer.surface.get_height()
            if layer.factor_x:
                screen.blit(layer.surface, (0, 0), (layer.posx - lw, layer.posy, sw, sh))
            if layer.factor_y:
                screen.blit(layer.surface, (0, 0), (layer.posx, layer.posy - lh, sw, sh))

    def update(self, lag_scalar):
        """apply queued parallax scroll or no-op"""
        if not any((self._queued_scroll_x, self._queued_scroll_y)):
            return
        for layer in self.layers:
            layer.scroll(self._queued_scroll_x * lag_scalar, self._queued_scroll_y * lag_scalar)
        # explicitly reset these or else the background does the jitterbug
        self._queued_scroll_x = self._queued_scroll_y = 0

    def scroll(self, scroll_x, scroll_y):
        """queue a parallax scroll for the next update"""
        self._queued_scroll_x, self._queued_scroll_y = scroll_x, scroll_y

    def add_layer(self, filepath, factor_x, factor_y, size=None):
        """Push a new image onto the background layer stack
           filepath is relative to images/
           factor_x sets the relative parallax scroll factor along the x axis
           factor_y sets the relative parallax scroll factor along the y axis

           in general, a higher scroll factor results in slower scrolling
           factor_x=0 disables scrolling on x
           factor_y=0 disables scrolling on y

           size applies a scale to the image loaded"""
        image = pygame.image.load(os.path.join('images', filepath)).convert_alpha()

        if size is not None:
            image = pygame.transform.scale(image, size)

        self.layers.append(ParallaxLayer(image, factor_x, factor_y))
