__author__ = 'cam'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os
import random

MOVE_SPEED = 1
WIDTH = 28
HEIGHT = 28
COLOR =  "#888888"

ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_RIGHT = ['tanks\h_right_1.png',
                   'tanks\h_right_2.png']
ANIMATION_LEFT = ['tanks\h_left_1.png',
                  'tanks\h_left_2.png']

ANIMATION_UP = ['tanks\h_up_1.png',
                'tanks\h_up_2.png']
ANIMATION_DOWN = ['tanks\h_down_1.png',
                  'tanks\h_down_2.png']

class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft,maxLengthUp):
        sprite.Sprite.__init__(self)

        self.image = Surface((WIDTH,HEIGHT))
        self.image = image.load("tanks\h_up_1.png")
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным

        self.startX = x # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up # скорость движения по вертикали, 0 - не двигается
        self.course = 1

        #  Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        #  Анимация движения вверх
        boltAnim = []
        for anim in ANIMATION_UP:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        # Анимация движения вниз
        boltAnim = []
        for anim in ANIMATION_DOWN:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

    def update(self, platforms): # по принципу героя

        #course - направление

        if self.course == 1:
            self.rect.y += self.yvel
            self.image.fill(Color(COLOR))
            self.boltAnimDown.blit(self.image, (0, 0))#animation
        elif self.course == 2:
            self.rect.x += self.xvel
            self.image.fill(Color(COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))#animation
        elif self.course == 3:
            self.rect.y -= self.yvel
            self.image.fill(Color(COLOR))
            self.boltAnimUp.blit(self.image, (0, 0))#animation
        elif self.course == 4:
            self.rect.x -= self.xvel
            self.image.fill(Color(COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))#animation

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
                if self.course == 1:
                    self.rect.y -= self.yvel
                elif self.course == 2:
                    self.rect.x -= self.xvel
                elif self.course == 3:
                    self.rect.y += self.yvel
                elif self.course == 4:
                    self.rect.x += self.xvel
                self.course = random.randint(1,4)
                #self.update(platforms)