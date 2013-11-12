# -*- coding: utf-8 -*-

from pygame import sprite, Rect

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

class Block(sprite.Sprite):
    """
        Данный класс описывает блоки
    """
    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT) # размеры блока

    def die(self, shutdirection):

        # попадание в блок
        if self.type == "-":

            # если он разрушаемый
            x = self.rect.left
            y = self.rect.top
            w = self.rect.width
            h = self.rect.height

            # уменьшаем размер блока с соответсвующего направления
            if shutdirection == "left":
                self.rect = Rect(x, y, w-8, h)
            elif shutdirection == "right":
                self.rect = Rect(x+8, y, w-8, h)
            if shutdirection == "up":
                self.rect = Rect(x, y, w, h-8)
            if shutdirection == "down":
                self.rect = Rect(x, y+8, w, h-8)

            # если блок уничтожен совсем, удаляем его из всех групп
            if (self.rect.width == 0) or (self.rect.height == 0):
                self.rect.width = self.rect.height = 0
                self.kill()