# -*- coding: utf-8 -*-

#from pygame import *
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


class Bullet(Widget):
    def __init__(self, x, y, shutdirection):

        # текстуры пули в разных направлениях
        self.b_u = Image('shut/bullet_up.png').texture
        self.b_r = Image('shut/bullet_right.png').texture
        self.b_d = Image('shut/bullet_down.png').texture
        self.b_l = Image('shut/bullet_left.png').texture

        # текстуры взрыва пули
        self.b_b_1 = Image('shut/bum_1.png').texture
        self.b_b_2 = Image('shut/bum_2.png').texture

        # скорость полета пули
        self.MOVE_SPEED = 5

        self.bum = 0     # индикатор взрыва пули

        # определяем направление полета
        if shutdirection == "":
            self.shutdirection = "up"
        else:
            self.shutdirection = shutdirection

        # загружаем картинку и определяем положение пули
        if shutdirection == "left":
            self.texture = self.b_l
            x += 0
            y += 11
        elif shutdirection == "right":
            self.texture = self.b_r
            x += 28
            y += 11
        elif shutdirection == "up":
            self.texture = self.b_u
            x += 11
            y += 28
        elif shutdirection == "down":
            self.texture = self.b_d
            x += 11
            y += 0

        # create a Widget object
        Widget.__init__(self, size=self.texture.size, pos=(x, y))
        # draw texture
        with self.canvas:
            self.rectangle = Rectangle(texture=self.texture, size=self.texture.size)

    def update(self, obstructions, anim):

        xvel = yvel = 0

        # определяем смещение пули
        if self.shutdirection == "left":
            xvel = -self.MOVE_SPEED  # Лево = x - n
        elif self.shutdirection == "right":
            xvel = self.MOVE_SPEED  # Право = x + n
        elif self.shutdirection == "up":
            yvel = self.MOVE_SPEED  # верх = y + n
        elif self.shutdirection == "down":
            yvel = -self.MOVE_SPEED  # низ = y - n
        elif self.shutdirection == "stop":
            xvel = yvel = 0

        self.x += xvel  # переносим своё положение на xvel и yvel
        self.y += yvel
        self.collide(xvel, yvel, obstructions)  # проверяем столкновения

        # если пуля начала взрываться
        if (0 < self.bum):

            # если пуля еще взрывается
            if (self.bum < 8):

                # анимация
                if anim:
                    self.rectangle.texture = self.b_b_1
                else:
                    self.rectangle.texture = self.b_b_2

                self.bum += 1  # флаг взрыва

            # если уже взорвалась
            else:
                self.shooter.isBullet = False  # сообщаем тому, кто выстрелил, что его пуля взорвалась
                self.parent.remove_widget(self)  # удаляем виджет из окна

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if self.collide_widget(p):  # если есть пересечение с чем то

                    self.x -= xvel  # переносим свои положение на -xvel
                    self.y -= yvel  # переносим свои положение на -yvel

                    # если пуля не начала взрываться, то начинаем взрывать ее
                    if self.bum == 0:
                        self.x -= 8  # 8 - потому что разница в размерах текстур пули и ее взрыва - 16 пикселей
                        self.y -= 8
                        self.size = self.b_b_1.size  # изменяем размер виджета
                        self.rectangle.size = self.b_b_1.size  # изменяем размер текстуры
                        self.bum = 1  # ставим флаг, что пуля начала взрываться
                        if self in self.list:
                            self.list.remove(self)  # удаляем пулю из массива пуль игроков

                        p.die(self.shutdirection)   # сообщаем объекту, в который попали, что в него попали

                        self.shutdirection = "stop"  # говорим, что пуля перестала лететь, взрывается на месте

    def die(self, shutdirection):
        # если пуля не начала взрываться, то начинаем взрывать ее
        if self.bum == 0:
            self.x -= 8  # 8 - потому что разница в размерах текстур пули и ее взрыва - 16 пикселей
            self.y -= 8
            self.size = self.b_b_1.size  # изменяем размер виджета
            self.rectangle.size = self.b_b_1.size  # изменяем размер текстуры
            self.bum = 1  # ставим флаг, что пуля начала взрываться
            if self in self.list:
                self.list.remove(self)  # удаляем пулю из массива пуль игроков

            self.shutdirection = "stop"  # говорим, что пуля перестала лететь, взрывается на месте