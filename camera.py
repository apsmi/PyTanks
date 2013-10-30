__author__ = 'cam'

from pygame import *

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+800 / 2, -t+600 / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-800), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-600), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)