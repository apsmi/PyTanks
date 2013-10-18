# -*- coding: utf-8 -*-

from pygame import *
import pyganim

class Tank_config():
    def __init__(self):
        self.START_X = 34
        self.START_Y = 34
        self.MOVE_SPEED_X = 1
        self.MOVE_SPEED_Y = 1
        self.WIDTH = 28
        self.HEIGHT = 28
        self.COLOR =  "#FFFFFF"
        self.ANIMATION_DELAY = 0.1 # скорость смены кадров
        self.ANIMATION_RIGHT = ['tanks\h_up_1.png',
                        'tanks\h_up_2.png']
        self.ANIMATION_LEFT = ['tanks\h_up_1.png',
                        'tanks\h_up_2.png']
        self.ANIMATION_UP = ['tanks\h_up_1.png',
                        'tanks\h_up_2.png']
        self.ANIMATION_DOWN = ['tanks\h_up_1.png',
                        'tanks\h_up_2.png']
        self.INIT_IMAGE = "tanks\h_up_1.png"


class Tank(sprite.Sprite):
    def __init__(self, config):
        sprite.Sprite.__init__(self)
        self.config = config
        self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
        self.rect = Rect(self.config.START_X, self.config.START_Y, self.config.WIDTH, self.config.HEIGHT) # прямоугольный объект

        self.image = image.load(self.config.INIT_IMAGE)

        self.xvel = 0 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 0 # скорость движения по вертикали, 0 - не двигается
        self.startX = self.config.START_X # начальные координаты
        self.startY = self.config.START_Y

        #  Анимация движения вправо
        boltAnim = []
        for anim in self.config.ANIMATION_RIGHT:
            boltAnim.append((anim, self.config.ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анимация движения влево
        boltAnim = []
        for anim in self.config.ANIMATION_LEFT:
            boltAnim.append((anim, self.config.ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        #  Анимация движения вверх
        boltAnim = []
        for anim in self.config.ANIMATION_UP:
            boltAnim.append((anim, self.config.ANIMATION_DELAY))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        # Анимация движения вниз
        boltAnim = []
        for anim in self.config.ANIMATION_DOWN:
            boltAnim.append((anim, self.config.ANIMATION_DELAY))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с танком

                if xvel > 0:                      # если движется вправо
                    self.rect.right -= xvel # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel # то не движется вверх

    def die(self):  #умираем, если попадает пуля
        self.rect.x = self.startX
        self.rect.y = self.startY