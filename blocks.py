# -*- coding: utf-8 -*-

from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32


class BlockWidget(Widget):

    def __init__(self, x, y, block_type):

        self.type = block_type     # тип платформы
        if block_type == "-":      # разрушаемая
            texture = Image("blocks/platform.png").texture
        else:  # type == "*":    # НЕразрушаемая
            texture = Image("blocks/beton.png").texture

        Widget.__init__(self, size=texture.size, pos=(x, y))

        with self.canvas:
            self.rectangle = Rectangle(texture=texture, size=texture.size)

    def die(self, shutdirection):

        # попадание в блок
        if self.type == "-":

            # если он разрушаемый
            w = self.width
            h = self.height

            # уменьшаем размер блока с соответсвующего направления, двигаем если нужно, правим текстуру
            # 8 потому что размер текстуры 32 пикселя, одно попадание - четверть блока сносит
            if shutdirection == "left":
                self.rectangle.texture = self.rectangle.texture.get_region(0, 0, w-8, h)
                self.size = self.rectangle.size = self.rectangle.texture.size

            elif shutdirection == "right":
                self.rectangle.texture = self.rectangle.texture.get_region(8, 0, w-8, h)
                self.size = self.rectangle.size = self.rectangle.texture.size
                self.x += 8

            elif shutdirection == "up":
                self.rectangle.texture = self.rectangle.texture.get_region(0, 8, w, h-8)
                self.size = self.rectangle.size = self.rectangle.texture.size
                self.y += 8

            elif shutdirection == "down":
                self.rectangle.texture = self.rectangle.texture.get_region(0, 0, w, h-8)
                self.size = self.rectangle.size = self.rectangle.texture.size

            # если блок уничтожен совсем, удаляем его из всех групп
            if (self.height == 0) or (self.width == 0):
                self.parent.blocks.remove(self)  # удаляем блок из массива блоков
                self.parent.remove_widget(self)  # удаляем виджет из окна