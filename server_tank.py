# -*- coding: utf-8 -*-

from pygame import sprite, Rect
import random

class Tank_config():
    """
      Данный класс описывает конфигурацию танка. Содержит только те свойства, которые влияют на поведение танка.
    """
    def __init__(self, min_x, max_x, min_y, max_y, speed, lifes, dead_count):
        self.dead_count = dead_count
        self.MIN_X = min_x                         # начальные координаты по горизрнтали
        self.MAX_X = max_x                         # начальные координаты по горизрнтали
        self.MIN_Y = min_y                         # начальные координаты по вертикали
        self.MAX_Y = max_y                         # начальные координаты по вертикали
        self.MOVE_SPEED = speed                     # скорость перемещения
        self.WIDTH = 28                           # ширина аватарки
        self.HEIGHT = 28                          # высота автарки
        self.lifeStart = lifes                        # количество жизней танка

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
        self.frag = 0                       # счетчик убийств
        self.xvel = 0                       # cкорость движения по горизонтали, 0 - стоит на месте
        self.yvel = 0                       # скорость движения по вертикали, 0 - не двигается
        self.dead = 0                       # счетчик кадров при смерти

        x = random.randint(self.config.MIN_X, self.config.MAX_X)
        y = random.randint(self.config.MIN_Y, self.config.MAX_Y)
        self.rect = Rect(x, y, self.config.WIDTH, self.config.HEIGHT) # прямоугольный объект

    def update(self,  obstructions):

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < self.config.dead_count):

                self.dead += 1 # счетчик кадров анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = random.randint(self.config.MIN_X, self.config.MAX_X)
                self.rect.y = random.randint(self.config.MIN_Y, self.config.MAX_Y)
                self.dead = 0
                self.course = ""
                self.shutdirection = "up"

        # если танк не взорван, то двигаем танк в соответсвующем направлении
        else:

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED                        # текущая скорость движения

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = -self.config.MOVE_SPEED

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = self.config.MOVE_SPEED

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

            return 1 # Взорвали танк. Если не взорвали, или взорвали не танк, то возвращаем 0.

        # если жизни еще есть
        else:

            # то их стало меньше
            self.life -= 1

        return 0