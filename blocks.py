__author__ = 'apsmi'

from pygame import *

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Platform(sprite.Sprite):
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        if type == "-":
            self.image = image.load("blocks/platform.png")
        elif type == "*":
            self.image = image.load("blocks/beton.png")
        else:
            self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)