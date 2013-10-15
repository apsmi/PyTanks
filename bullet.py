# -*- coding: utf-8 -*-
__author__ = 'apsmi'

from pygame import *
import pyganim

MOVE_SPEED = 5
WIDTH = 6
HEIGHT = 6
BUM_WIDTH = 22
BUM_HEIGHT = 22
COLOR =  "#333333"

ANIMATION_DELAY = 0.1 # скорость смены кадров
ANIMATION_BUM = ['shut/bum_1.png',
                 'shut/bum_2.png']

class Bullet(sprite.Sprite):
    def __init__(self, x, y, shutdirection):
        sprite.Sprite.__init__(self)
        self.bum = 0
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))

        self.shutdirection = shutdirection
        if shutdirection == "left":
            self.image = image.load("shut/bullet_left.png")
            self.startX -= 6
            self.startY += 11
        elif shutdirection == "right":
            self.image = image.load("shut/bullet_right.png")
            self.startX += 28
            self.startY += 11
        elif shutdirection == "up":
            self.image = image.load("shut/bullet_up.png")
            self.startX += 11
            self.startY += 6
        elif shutdirection == "down":
            self.image = image.load("shut/bullet_down.png")
            self.startX += 11
            self.startY += 28

        self.rect = Rect(self.startX, self.startY, WIDTH, HEIGHT) # прямоугольный объект

    def update(self, platforms):

        left = right = up = down = False

        if self.shutdirection == "left":
            left = True
        if self.shutdirection == "right":
            right = True
        if self.shutdirection == "up":
            up = True
        if self.shutdirection == "down":
            down = True
        if self.shutdirection == "stop":
            left = right = up = down = False

        if left:
            self.xvel = -MOVE_SPEED # Лево = x - n

        if right:
            self.xvel = MOVE_SPEED # Право = x + n

        if not(left or right): # стоим, когда нет указаний идти вправо - влево
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms) #проверяем столкновения

        if up:
            self.yvel = -MOVE_SPEED # верх = x- n

        if down:
            self.yvel = MOVE_SPEED # низ = x + n

        if not(up or down): # стоим, когда нет указаний идти вправо - влево
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, platforms)#проверяем столкновения

        if (0 < self.bum):
            if (self.bum < 20):
                self.image.fill(Color(COLOR))
                self.boltAnimBum.blit(self.image, (0, 0))  #animation
                self.bum += 1

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if self.bum == 0:
                    self.image = Surface((BUM_WIDTH,BUM_HEIGHT))
                    self.rect = Rect(self.rect.left - 8, self.rect.top-8, BUM_WIDTH, BUM_HEIGHT) # прямоугольный объект
                    self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
                    #  Анимация движения вправо
                    boltAnim = []
                    for anim in ANIMATION_BUM:
                        boltAnim.append((anim, ANIMATION_DELAY))
                    self.boltAnimBum = pyganim.PygAnimation(boltAnim)
                    self.boltAnimBum.play()
                    self.image.fill(Color(COLOR))
                    self.boltAnimBum.blit(self.image, (0, 0))  #animation
                    self.bum = 1

                if xvel > 0:                      # если движется вправо
                    self.rect.right -= xvel # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel # то не движется вверх

                self.shutdirection = "stop"