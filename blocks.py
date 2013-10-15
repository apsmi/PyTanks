# -*- coding: utf-8 -*-
__author__ = 'apsmi'

from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Platform(sprite.Sprite):
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        self.type = type
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        if type == "-":
            self.image = image.load("blocks/platform.png")
        elif type == "*":
            self.image = image.load("blocks/beton.png")
        else:
            self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def shut(self, shutdirection):
        if self.type == "-":
            x = self.rect.left
            y = self.rect.top
            w = self.rect.width
            h = self.rect.height

            if shutdirection == "left":
                self.image = self.image.subsurface((0, 0, w-8, h))
                self.rect = Rect(x, y, w-8, h)
            elif shutdirection == "right":
                self.image = self.image.subsurface((8, 0, w-8, h))
                self.rect = Rect(x+8, y, w-8, h)
            if shutdirection == "up":
                self.image = self.image.subsurface((0, 0, w, h-8))
                self.rect = Rect(x, y, w, h-8)
            if shutdirection == "down":
                self.image = self.image.subsurface((0, 8, w, h-8))
                self.rect = Rect(x, y+8, w, h-8)

            if (self.rect.width == 0) or (self.rect.height == 0):
                self.rect.width = self.rect.height = 0
                self.kill()