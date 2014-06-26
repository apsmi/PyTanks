# -*- coding: utf-8 -*-

from pygame import sprite, Rect
from kivy.core.image import Image

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

class Block(sprite.Sprite):
    """
        Данный класс описывает блоки
    """

    def __init__(self, x, y, type):
        sprite.Sprite.__init__(self)

        #self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)) # изображение
        #self.texture = Image("player1_1.png").texture

        self.type = type     # тип платформы
        if type == "-":      # разрушаемая
            self.texture = Image("blocks/platform.png").texture
        elif type == "*":    # НЕразрушаемая
            self.texture = Image("blocks/beton.png").texture
        #else:                # все остальные
            #self.image.fill(Color(PLATFORM_COLOR))

        self.rect = Rect((x, y), self.texture.size)  # размеры блока

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
                self.texture = self.texture.get_region(0, 0, w-8, h)
                self.rect = Rect(x, y, w-8, h)
            elif shutdirection == "right":
                self.texture = self.texture.get_region(8, 0, w-8, h)
                self.rect = Rect(x+8, y, w-8, h)
            if shutdirection == "up":
                self.texture = self.texture.get_region(0, 8, w, h-8)
                self.rect = Rect(x, y+8, w, h-8)
            if shutdirection == "down":
                self.texture = self.texture.get_region(0, 0, w, h-8)
                self.rect = Rect(x, y, w, h-8)

            # если блок уничтожен совсем, удаляем его из всех групп
            if (self.rect.width == 0) or (self.rect.height == 0):
                self.rect.width = self.rect.height = 0
                self.kill()