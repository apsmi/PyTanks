# -*- coding: utf-8 -*-
__author__ = 'cam'


class NewCamera(object):

    def __init__(self, level_width, level_height, window_width, window_height):
        self.level_width, self.level_height, self.window_width, self.window_height = \
            level_width, level_height, window_width, window_height
        self.window_x = 0
        self.window_y = 0

    def update(self, target):
        window_x = target.x - self.window_width/2  # window(x, y) in level coordinates
        window_x = max(0, window_x)
        window_x = min(window_x, self.level_width - self.window_width)
        self.window_x = window_x

        window_y = target.y - self.window_height/2  # window(x, y) in level coordinates
        window_y = max(0, window_y)
        window_y = min(window_y, self.level_height - self.window_height)
        self.window_y = window_y

        print(target.pos)

    def apply(self, entity):
        x, y = entity.pos[0], entity.pos[1]
        x -= self.window_x
        y -= self.window_y
        return (x, y)