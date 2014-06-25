# -*- coding: utf-8 -*-

from pygame import *
import pyganim
from kivy.core.image import Image

class Bullet(sprite.Sprite):
    def __init__(self, x, y, shutdirection):
        sprite.Sprite.__init__(self)

        self.IMAGE_LEFT = "shut/bullet_left.png"
        self.IMAGE_RIGHT = "shut/bullet_right.png"
        self.IMAGE_UP = "shut/bullet_up.png"
        self.IMAGE_DOWN = "shut/bullet_down.png"
        self.ANIMATION_DELAY = 0.1 # скорость смены кадров
        self.ANIMATION_BUM = ['shut/bum_1.png',
                 'shut/bum_2.png']
        self.MOVE_SPEED = 5
        self.BUM_WIDTH = 22
        self.BUM_HEIGHT = 22
        self.COLOR =  "#FFFFFF"

        self.bum = 0    # индикатор взрыва пули
        self.xvel = 0   # скорость полета пули
        self.yvel = 0   # скорость полета пули
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

        # определяем направление полета
        if shutdirection == "":
            self.shutdirection = "up"
        else:
            self.shutdirection = shutdirection

        #self.image = Surface((self.WIDTH,self.HEIGHT)) # поверхность изображения

        # загружаем картинку и определяем положение пули
        if shutdirection == "left":
            self.texture = Image(self.IMAGE_LEFT).texture
            self.startX -= 6
            self.startY += 11
        elif shutdirection == "right":
            self.texture = Image(self.IMAGE_RIGHT).texture
            self.startX += 28
            self.startY += 11
        elif shutdirection == "up":
            self.texture = Image(self.IMAGE_UP).texture
            self.startX += 11
            self.startY += 6
        elif shutdirection == "down":
            self.texture = Image(self.IMAGE_DOWN).texture
            self.startX += 11
            self.startY += 28

        self.rect = Rect(self.startX, self.startY, self.WIDTH, self.HEIGHT) # прямоугольный объект

    def update(self, obstructions):

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
            self.xvel = -self.MOVE_SPEED # Лево = x - n

        if right:
            self.xvel = self.MOVE_SPEED # Право = x + n

        if not(left or right): # стоим, когда нет указаний идти вправо-влево или попали куда-то
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, obstructions) #проверяем столкновения

        if up:
            self.yvel = -self.MOVE_SPEED # верх = x- n

        if down:
            self.yvel = self.MOVE_SPEED # низ = x + n

        if not(up or down): # стоим, когда нет указаний идти вправо - влево или попали куда-то
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, obstructions)#проверяем столкновения

        if (0 < self.bum):
            if (self.bum < 20):
                #self.image = Surface((self.BUM_WIDTH,self.BUM_HEIGHT))
                self.rect = Rect(self.rect.left, self.rect.top, self.BUM_WIDTH, self.BUM_HEIGHT) # прямоугольный объект
                #self.image.fill(Color(self.COLOR))
                #self.image.set_colorkey(Color(self.COLOR)) # делаем фон прозрачным
                #self.boltAnimBum.blit(self.image, (0, 0))  #animation
                self.texture = Image('shut/bum_2.png').texture  # TODO: port animation to kivy
                self.bum += 1
            else:
                self.kill()
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
                    self.rect.right -= xvel # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel # то не движется вверх

                self.shutdirection = "stop"

    def die(self, shutdirection):
        return 0