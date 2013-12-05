# -*- coding: utf-8 -*-

from pygame import sprite, Rect

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

class Block(sprite.Sprite):
    """
        Данный класс описывает блоки
    """
    def __init__(self, x, y, type, id, demage):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT) # размеры блока
        self.type = type
        self.id = id
        self.shooted = False
        self.dead = False
        self.shootdirection = ""
        self.demage = demage
        self.hits = []

    def die(self, shutdirection):

        # попадание в блок
        if self.type == "-":
            self.shooted = True
            self.shootdirection = shutdirection
            self.hits.append(shutdirection)

            # если он разрушаемый
            x = self.rect.left
            y = self.rect.top
            w = self.rect.width
            h = self.rect.height

            # уменьшаем размер блока с соответсвующего направления
            if shutdirection == "left":
                self.rect = Rect(x, y, w-self.demage, h)
            elif shutdirection == "right":
                self.rect = Rect(x+self.demage, y, w-self.demage, h)
            if shutdirection == "up":
                self.rect = Rect(x, y, w, h-self.demage)
            if shutdirection == "down":
                self.rect = Rect(x, y+self.demage, w, h-self.demage)

            # если блок уничтожен совсем, удаляем его из всех групп
            if (self.rect.width == 0) or (self.rect.height == 0):
                self.rect.width = self.rect.height = 0
                #self.kill()
                self.dead = True