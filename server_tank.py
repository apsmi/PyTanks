# -*- coding: utf-8 -*-

from pygame import sprite, Surface, Rect, image, Color, transform

import pyganim


class Tank_config():
    """
      Данный класс описывает конфигурацию танка. Содержит только те свойства, которые влияют на поведение танка.
    """
    def __init__(self, x, y):
        self.START_X = x                         # начальные координаты по горизрнтали
        self.START_Y = y                         # начальные координаты по вертикали
        self.MOVE_SPEED_X = 1                     # скорость перемещения по горизонтали
        self.MOVE_SPEED_Y = 1                     # скорость перемещения по вертикали
        self.WIDTH = 28                           # ширина аватарки
        self.HEIGHT = 28                          # высота автарки
        self.lifeStart = 1                        # количество жизней танка
        self.last = {}                            #x,y,course,shutdirection

class Tank(sprite.Sprite):
    """
        Это основной класс, реализующий поведение танка.
    """

    def __init__(self, config):
        sprite.Sprite.__init__(self)

        self.config = config

        self.course = ""                 # направление движения
        self.shutdirection = "up"           # направление выстрела
        self.isBullet = False               # флаг существования пули
        self.life = self.config.lifeStart   # оставшееся количество жизней
        self.xvel = 0                       # cкорость движения по горизонтали, 0 - стоит на месте
        self.yvel = 0                       # скорость движения по вертикали, 0 - не двигается
        self.dead = 0                       # счетчик кадров при смерти

    def update(self,  obstructions):

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 30):

                self.dead += 1 # счетчик кадров анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = self.config.START_X
                self.rect.y = self.config.START_Y
                self.dead = 0
                self.course = ""
                self.shutdirection = "up"

        # если танк не взорван, то двигаем танк в соответсвующем направлении
        else:

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED_X                        # текущая скорость движения

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = -self.config.MOVE_SPEED_Y

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = self.config.MOVE_SPEED_Y

            # стоим, когда нет указаний идти вверх - вниз
            else:
                self.yvel = 0

            self.rect.y += self.yvel                 # переносим свои положение на yvel
            self.collide(0, self.yvel, obstructions) # проверяем столкновения

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if sprite.collide_rect(self, p): # если есть пересечение чего-то с танком

                    if xvel > 0:                 # если движется вправо
                        self.rect.right -= xvel  # то не движется вправо

                    if xvel < 0:                 # если движется влево
                        self.rect.left -= xvel   # то не движется влево

                    if yvel > 0:                 # если падает вниз
                        self.rect.bottom -= yvel # то не падает вниз

                    if yvel < 0:                 # если движется вверх
                        self.rect.top -= yvel    # то не движется вверх

    def die(self, shutdirection):

        # умираем, если попадает пуля
        # если попадание последнее
        if self.life == 1:

            # начинаем взрыывать танк
            self.dead = 1
            self.life = self.config.lifeStart

        # если жизни еще есть
        else:

            # то их стало меньше
            self.life -= 1