# -*- coding: utf-8 -*-

from pygame import *
from kivy.core.image import Image

class Bullet(sprite.Sprite):
    def __init__(self, x, y, shutdirection):
        sprite.Sprite.__init__(self)

        self.b_u = Image('shut/bullet_up.png').texture
        self.b_r = Image('shut/bullet_right.png').texture
        self.b_d = Image('shut/bullet_down.png').texture
        self.b_l = Image('shut/bullet_left.png').texture

        self.b_b_1 = Image('shut/bum_1.png').texture
        self.b_b_2 = Image('shut/bum_2.png').texture

        self.MOVE_SPEED = 5
        self.BUM_WIDTH = 22
        self.BUM_HEIGHT = 22

        self.bum = 0     # индикатор взрыва пули
        self.xvel = 0    # скорость полета пули
        self.yvel = 0    # скорость полета пули
        self.startX = x  # начальная позиция
        self.startY = y  # начальная позиция
        self.WIDTH = 6   # ширина картинки
        self.HEIGHT = 6  # высота картинки

        # определяем направление полета
        if shutdirection == "":
            self.shutdirection = "up"
        else:
            self.shutdirection = shutdirection

        # загружаем картинку и определяем положение пули
        if shutdirection == "left":
            self.texture = self.b_l
            self.startX += 0
            self.startY += 11
        elif shutdirection == "right":
            self.texture = self.b_r
            self.startX += 28
            self.startY += 11
        elif shutdirection == "up":
            self.texture = self.b_u
            self.startX += 11
            self.startY += 28
        elif shutdirection == "down":
            self.texture = self.b_d
            self.startX += 11
            self.startY += 0

        self.rect = Rect(self.startX, self.startY, self.WIDTH, self.HEIGHT) # прямоугольный объект

    def update(self, obstructions, anim):

        self.xvel = self.yvel = 0

        if self.shutdirection == "left":
            self.xvel = -self.MOVE_SPEED  # Лево = x - n
        elif self.shutdirection == "right":
            self.xvel = self.MOVE_SPEED  # Право = x + n
        elif self.shutdirection == "up":
            self.yvel = self.MOVE_SPEED  # верх = y + n
        elif self.shutdirection == "down":
            self.yvel = -self.MOVE_SPEED  # низ = y - n
        elif self.shutdirection == "stop":
            self.xvel = self.yvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, obstructions)  # проверяем столкновения

        self.rect.y += self.yvel  # переносим свои положение на yvel
        self.collide(0, self.yvel, obstructions)  # проверяем столкновения

        if (0 < self.bum):
            if (self.bum < 8):
                self.rect = Rect(self.rect.left, self.rect.top, self.BUM_WIDTH, self.BUM_HEIGHT)  # прямоугольный объект
                if anim:
                    self.texture = self.b_b_1
                else:
                    self.texture = self.b_b_2
                self.bum += 1
            else:
                self.kill()
                self.picture.size = (0, 0)
                self.shooter.isBullet = False # сообщаем тому, кто выстрелил, что его пуля кердык

    def collide(self, xvel, yvel, obstructions):

        for p in obstructions:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                #если пуля не начала взрываться, то начинаем взрывать ее
                if self.bum == 0:
                    self.rect.left -= 8
                    self.rect.top -= 8
                    self.bum = 1
                    p.die(self.shutdirection)   # сообщаем объекту, в который попали, что в него попали

                if xvel > 0:                      # если движется вправо
                    self.rect.right -= xvel  # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel  # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel  # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel  # то не движется вверх

                self.shutdirection = "stop"

    def die(self, shutdirection):
        return 0