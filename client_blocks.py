# -*- coding: utf-8 -*-

from pygame import sprite, Surface, image, Rect, Color

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Block(sprite.Sprite):
    """
        Данный класс описывает блоки
    """
    def __init__(self, id, x, y, type, DEMAGE):
        sprite.Sprite.__init__(self)

        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)) # изображение

        self.id = id        # идентификатор
        self.type = type     # тип платформы
        self.demage = DEMAGE

        if type == "-":      # разрушаемая
            self.image = image.load("blocks/platform.png")
        elif type == "*":    # НЕразрушаемая
            self.image = image.load("blocks/beton.png")
        else:                # все остальные
            self.image.fill(Color(PLATFORM_COLOR))

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
                self.image = self.image.subsurface((0, 0, w-self.demage, h))
                self.rect = Rect(x, y, w-self.demage, h)
            elif shutdirection == "right":
                self.image = self.image.subsurface((self.demage, 0, w-self.demage, h))
                self.rect = Rect(x+self.demage, y, w-self.demage, h)
            if shutdirection == "up":
                self.image = self.image.subsurface((0, 0, w, h-self.demage))
                self.rect = Rect(x, y, w, h-self.demage)
            if shutdirection == "down":
                self.image = self.image.subsurface((0, self.demage, w, h-self.demage))
                self.rect = Rect(x, y+self.demage, w, h-self.demage)

            # если блок уничтожен совсем, удаляем его из всех групп
            if (self.rect.width == 0) or (self.rect.height == 0):
                self.rect.width = self.rect.height = 0
                self.kill()