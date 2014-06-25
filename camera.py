# -*- coding: utf-8 -*-
__author__ = 'cam'

from pygame import *

class Camera(object):
    def __init__(self, camera_func, width, height, display_w, display_h):
        self.camera_func = camera_func
        self.display_w, self.display_h = display_w, display_h
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, self.display_w, self.display_h)


def camera_configure(camera, target_rect, display_w, display_h):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+display_w / 2, -t+display_h / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-display_w), l)         # Не движемся дальше правой границы
    t = max(-(camera.height-display_h), t)        # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)