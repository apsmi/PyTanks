# -*- coding: utf-8 -*-

from pygame import sprite, Rect

from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

import random


class TankWidget(Widget):

    def __init__(self):

        WIDTH = 28                           # ширина аватарки
        HEIGHT = 28                          # высота автарки
        START_X = random.randint(40, 600)                         # начальные координаты по горизрнтали
        START_Y = random.randint(40, 400)                         # начальные координаты по вертикали

        self.t_u_1 = Image('tanks/player_u_1.png').texture
        self.t_u_2 = Image('tanks/player_u_2.png').texture
        self.t_r_1 = Image('tanks/player_r_1.png').texture
        self.t_r_2 = Image('tanks/player_r_2.png').texture
        self.t_d_1 = Image('tanks/player_d_1.png').texture
        self.t_d_2 = Image('tanks/player_d_2.png').texture
        self.t_l_1 = Image('tanks/player_l_1.png').texture
        self.t_l_2 = Image('tanks/player_l_2.png').texture

        self.t_b_2 = Image('tanks/die_2.png').texture
        self.t_b_3 = Image('tanks/die_3.png').texture

        # create a Widget object
        Widget.__init__(self, size=(WIDTH, HEIGHT), pos=(START_X, START_Y))

        with self.canvas:
            self.rectangle = Rectangle(texture=self.t_u_1, size=self.t_u_1.size)

        self.MOVE_SPEED_X = 2                     # скорость перемещения по горизонтали
        self.MOVE_SPEED_Y = 2                     # скорость перемещения по вертикали
        self.lifeStart = 1                        # количество жизней танка
        self.course = ""                 # направление движения
        self.shutdirection = "up"           # направление выстрела
        self.isBullet = False               # флаг существования пули
        self.life = self.lifeStart   # оставшееся количество жизней
        self.dead = 0                       # счетчик кадров при смерти

    def update(self,  obstructions, anim):

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 15):

                if anim:                                    # TODO: подумать над тем, как не присваивать каждый раз
                    self.rectangle.texture = self.t_b_2
                else:
                    self.rectangle.texture = self.t_b_3
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                x = random.randint(40, 600)
                y = random.randint(40, 400)
                self.pos = (x, y)

                self.dead = 0
                self.rectangle.texture = self.t_u_1
                self.course = ""
                self.shutdirection = "up"

        # если танк не взорван, то двигаем танк в соответсвующем направлении
        else:

            #обнуляем движение
            xvel = yvel = 0

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                xvel = -self.MOVE_SPEED_X                        # текущая скорость движения

                if anim:
                    self.rectangle.texture = self.t_l_1
                else:
                    self.rectangle.texture = self.t_l_2

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                xvel = self.MOVE_SPEED_X

                if anim:
                    self.rectangle.texture = self.t_r_1
                else:
                    self.rectangle.texture = self.t_r_2

            # движение вверх
            elif self.course == "up":
                self.shutdirection = "up"
                yvel = self.MOVE_SPEED_Y

                if anim:
                    self.rectangle.texture = self.t_u_1
                else:
                    self.rectangle.texture = self.t_u_2

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                yvel = -self.MOVE_SPEED_Y

                if anim:
                    self.rectangle.texture = self.t_d_1
                else:
                    self.rectangle.texture = self.t_d_2

            self.pos[0] += xvel                 # переносим свои положение на xvel
            self.pos[1] += yvel                 # переносим свои положение на yvel

            self.collide(xvel, yvel, obstructions)  # проверяем столкновения

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if self.collide_widget(p):  # если есть пересечение чего-то с танком

                    self.pos[0] -= xvel                 # переносим свои положение на -xvel
                    self.pos[1] -= yvel                 # переносим свои положение на -yvel

    def die(self, shutdirection):

        # умираем, если попадает пуля
        # если попадание последнее
        if self.life == 1:

            # начинаем взрыывать танк
            self.dead = 1
            self.life = self.lifeStart

        # если жизни еще есть
        else:

            # то их стало меньше
            self.life -= 1



# TODO: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TODO: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TODO: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TODO: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TODO: +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Tank_config():
    """
      Данный класс описывает конфигурацию танка. Содержит только те свойства, которые влияют на поведение танка.
    """
    def __init__(self):
        self.START_X = random.randint(40, 600)                         # начальные координаты по горизрнтали
        self.START_Y = random.randint(40, 400)                         # начальные координаты по вертикали
        self.MOVE_SPEED_X = 2                     # скорость перемещения по горизонтали
        self.MOVE_SPEED_Y = 2                     # скорость перемещения по вертикали
        self.WIDTH = 28                           # ширина аватарки
        self.HEIGHT = 28                          # высота автарки
        self.lifeStart = 1                        # количество жизней танка

        self.t_u_1 = Image('tanks/player_u_1.png').texture
        self.t_u_2 = Image('tanks/player_u_2.png').texture
        self.t_r_1 = Image('tanks/player_r_1.png').texture
        self.t_r_2 = Image('tanks/player_r_2.png').texture
        self.t_d_1 = Image('tanks/player_d_1.png').texture
        self.t_d_2 = Image('tanks/player_d_2.png').texture
        self.t_l_1 = Image('tanks/player_l_1.png').texture
        self.t_l_2 = Image('tanks/player_l_2.png').texture

        self.t_b_2 = Image('tanks/die_2.png').texture
        self.t_b_3 = Image('tanks/die_3.png').texture


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
        self.COLOR = "#000000"             # цвет фона аватарки

        # автарка танка
        self.texture = self.config.t_u_1
        self.rect = Rect(self.config.START_X, self.config.START_Y, self.config.WIDTH, self.config.HEIGHT)  # прямоугольный объект

    def update(self,  obstructions, anim):

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 15):

                if anim:
                    self.texture = self.config.t_b_2
                else:
                    self.texture = self.config.t_b_3
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = random.randint(40, 600)
                self.rect.y = random.randint(40, 400)
                self.dead = 0
                self.texture = self.config.t_u_1
                self.course = ""
                self.shutdirection = "up"

        # если танк не взорван, то двигаем танк в соответсвующем направлении
        else:

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED_X                        # текущая скорость движения

                if anim:
                    self.texture = self.config.t_l_1
                else:
                    self.texture = self.config.t_l_2

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X
                if anim:
                    self.texture = self.config.t_r_1
                else:
                    self.texture = self.config.t_r_2

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = self.config.MOVE_SPEED_Y
                if anim:
                    self.texture = self.config.t_u_1
                else:
                    self.texture = self.config.t_u_2

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = -self.config.MOVE_SPEED_Y
                if anim:
                    self.texture = self.config.t_d_1
                else:
                    self.texture = self.config.t_d_2

            # стоим, когда нет указаний идти вверх - вниз
            else:
                self.yvel = 0

            self.rect.y += self.yvel                 # переносим свои положение на yvel
            self.collide(0, self.yvel, obstructions) # проверяем столкновения

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if sprite.collide_rect(self, p):  # если есть пересечение чего-то с танком

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