# -*- coding: utf-8 -*-

from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

import random


class TankWidget(Widget):

    def __init__(self):

        WIDTH = 28                           # ширина аватарки
        HEIGHT = 28                          # высота автарки
        self.START_X = random.randint(40, 600)                         # начальные координаты по горизрнтали
        self.START_Y = random.randint(40, 400)                         # начальные координаты по вертикали

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
        Widget.__init__(self, size=(WIDTH, HEIGHT), pos=(self.START_X, self.START_Y))

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
                self.dead += 1  # счетчик кадров анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.START_X = random.randint(40, 600)
                self.START_Y = random.randint(40, 400)
                self.pos = (self.START_X, self.START_Y)

                self.dead = 0
                self.rectangle.texture = self.t_u_1
                self.course = ""
                self.shutdirection = "up"

                self.parent.players.append(self)  # включаем танк в массив танков

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

            self.x += xvel                 # переносим свои положение на xvel
            self.y += yvel                 # переносим свои положение на yvel

            self.collide(xvel, yvel, obstructions)  # проверяем столкновения

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if self.collide_widget(p):  # если есть пересечение чего-то с танком

                    self.x -= xvel                 # переносим свои положение на -xvel
                    self.y -= yvel                 # переносим свои положение на -yvel

                    return True  # если есть столкновение - ставим флаг (для монстров - они поворачиваются)

        return False

    def die(self, shutdirection):

        # если попадание последнее
        if self.life == 1:

            # начинаем взрыывать танк
            self.dead = 1
            self.life = self.lifeStart
            # умираем, если попадает пуля
            if self in self.parent.monsters:
                self.parent.monsters.remove(self)  # удаляем танк из массива танков
            if self in self.parent.players:
                self.parent.players.remove(self)  # удаляем танк из массива танков

        # если жизни еще есть
        else:

            # то их стало меньше
            self.life -= 1


class Player(TankWidget):
    def __init__(self):
        TankWidget.__init__(self)
        with self.canvas:
            self.rectangle = Rectangle(texture=self.t_u_1, size=self.t_u_1.size)