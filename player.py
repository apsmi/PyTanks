# -*- coding: utf-8 -*-

from pygame import *
import pyganim

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


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.yvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH,HEIGHT))
        self.image = image.load("tanks\h_up_1.png")
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект

        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
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

    def update(self,  left, right, up, down, platforms):
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
            self.image.fill(Color(COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))  #animation

        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))#animation

        if not(left or right): # стоим, когда нет указаний идти вправо - влево
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms) #проверяем столкновения

        if up:
            self.yvel = -MOVE_SPEED # верх = x- n
            self.image.fill(Color(COLOR))
            self.boltAnimUp.blit(self.image, (0, 0))#animation

        if down:
            self.yvel = MOVE_SPEED # низ = x + n
            self.image.fill(Color(COLOR))
            self.boltAnimDown.blit(self.image, (0, 0))#animation

        if not(up or down): # стоим, когда нет указаний идти вправо - влево
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, platforms)#проверяем столкновения

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right -= xvel # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel # то не движется вверх