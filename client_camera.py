# -*- coding: utf-8 -*-
__author__ = 'cam'

from pygame import *

class Camera(object):
    def __init__(self, camera_func, width, height, WINDOW_W, WINDOW_H):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target, WINDOW_W, WINDOW_H):
        self.state = self.camera_func(self.state, target.rect, WINDOW_W, WINDOW_H)


def camera_configure(camera, target_rect, WINDOW_W, WINDOW_H):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WINDOW_W / 2, -t+WINDOW_H / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WINDOW_W), l)         # Не движемся дальше правой границы
    t = max(-(camera.height-WINDOW_H), t)        # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)