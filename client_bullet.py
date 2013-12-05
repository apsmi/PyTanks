# -*- coding: utf-8 -*-

import pyganim
from pygame import *

BUM_COUNT = 10

class Bullet(sprite.Sprite):
    def __init__(self, id, x, y, shutdirection):
        sprite.Sprite.__init__(self)

        self.IMAGE_LEFT = "shut/bullet_left.png"
        self.IMAGE_RIGHT = "shut/bullet_right.png"
        self.IMAGE_UP = "shut/bullet_up.png"
        self.IMAGE_DOWN = "shut/bullet_down.png"
        self.ANIMATION_DELAY = 0.1 # скорость смены кадров
        self.ANIMATION_BUM = ['shut/bum_1.png',
                 'shut/bum_2.png']

        self.BUM_WIDTH = 22
        self.BUM_HEIGHT = 22
        self.COLOR =  "#FFFFFF"

        self.id = id

        self.startX = x # начальная позиция
        self.startY = y # начальная позиция
        self.WIDTH = 6  # ширина картинки
        self.HEIGHT = 6 # высота картинки

        #  Анимация взрыва пули
        boltAnim = []
        for anim in self.ANIMATION_BUM:
            boltAnim.append((anim, self.ANIMATION_DELAY))
        self.boltAnimBum = pyganim.PygAnimation(boltAnim)
        self.boltAnimBum.play()

        self.image = Surface((self.WIDTH,self.HEIGHT)) # поверхность изображения

        # загружаем картинку и определяем положение пули
        if shutdirection == "left":
            self.image = image.load(self.IMAGE_LEFT)

        elif shutdirection == "right":
            self.image = image.load(self.IMAGE_RIGHT)

        elif shutdirection == "up":
            self.image = image.load(self.IMAGE_UP)

        elif shutdirection == "down":
            self.image = image.load(self.IMAGE_DOWN)

        self.rect = Rect(self.startX, self.startY, self.WIDTH, self.HEIGHT) # прямоугольный объект

    def update(self, x, y, bum):

        self.rect.x, self.rect.y, self.bum = x, y, bum

        if (0 < self.bum):
            if (self.bum < BUM_COUNT):
                self.image = Surface((self.BUM_WIDTH,self.BUM_HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR)) # делаем фон прозрачным
                self.boltAnimBum.blit(self.image, (0, 0))  #animation
            else:
                self.kill()