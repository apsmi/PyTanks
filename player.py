#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *

MOVE_SPEED = 2
WIDTH = 32
HEIGHT = 32
COLOR =  "#888888"


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект

    def update(self,  left, right, up, down, platforms):
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED # Право = x + n

        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms) #проверяем столкновения

        if up:
            self.yvel = -MOVE_SPEED # верх = x- n

        if down:
            self.yvel = MOVE_SPEED # низ = x + n

        if not(left or right): # стоим, когда нет указаний идти вправо - влево
            self.xvel = 0

        if not(up or down): # стоим, когда нет указаний идти вправо - влево
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, platforms)#проверяем столкновения

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх