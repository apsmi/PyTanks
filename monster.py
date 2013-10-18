__author__ = 'cam'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import random
from tank import Tank

class Monster(Tank):
    def __init__(self, config):
        Tank.__init__(self, config)

        self.course = 1 # направление движения
        self.isBullet = False # проверка существовая пули
        self.shutdirection = "down" # направления выстела
        self.fire = 0 # выстрел
        self.impact = False # переменная столкновения

    def update(self, platforms, hero_y, hero_x): # по принципу героя

        #наведение на героя

        if self.config.counter == 0:
            if 50 < random.randint (1,100) and hero_y != self.rect.y:
                if self.impact == False:
                    if hero_y > self.rect.y:
                        self.course = 1
                    elif hero_y < self.rect.y:
                        self.course = 3
            else:
                if self.impact == False:
                    if hero_x > self.rect.x:
                        self.course = 2
                    elif hero_x < self.rect.x:
                        self.course = 4
            self.config.counter = 15


        #проверка на макс. пройденое расстояние
        if (abs(self.startX - self.rect.x) > self.config.maxLengthLeft):
            self.course = 2
            self.config.counter = 200
            #self.config.xvel =-self.config.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.config.maxLengthUp):
            self.course = 1
            self.config.counter = 200
            #self.config.yvel = -self.config.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль


        #course - направление
        #движение
        if self.course == 1:
            self.rect.y += self.config.yvel
            self.image.fill(Color(self.config.COLOR))
            self.boltAnimDown.blit(self.image, (0, 0))#animation
            self.image = transform.rotate(self.image, 180)
            self.shutdirection = "down"
            self.collide(0, self.config.yvel, platforms) #проверяем столкновения
        elif self.course == 2:
            self.rect.x += self.config.xvel
            self.image.fill(Color(self.config.COLOR))
            self.boltAnimRight.blit(self.image, (0, 0))#animation
            self.shutdirection = "right"
            self.image = transform.rotate(self.image, 270)
            self.collide(self.config.xvel, 0, platforms) #проверяем столкновения
        elif self.course == 3:
            self.rect.y -= self.config.yvel
            self.image.fill(Color(self.config.COLOR))
            self.boltAnimUp.blit(self.image, (0, 0))#animation
            self.shutdirection = "up"
            self.collide(0, -self.config.yvel, platforms) #проверяем столкновения
        elif self.course == 4:
            self.rect.x -= self.config.xvel
            self.image.fill(Color(self.config.COLOR))
            self.boltAnimLeft.blit(self.image, (0, 0))#animation
            self.image = transform.rotate(self.image, 90)
            self.shutdirection = "left"
            self.collide(-self.config.xvel, 0, platforms) #проверяем столкновения


        if self.impact == True:
            if hero_y == self.rect.y:
                if hero_x > self.rect.x:
                    self.course = 2
                elif hero_x < self.rect.x:
                    self.course = 4

            if hero_x == self.rect.x:
                if hero_y > self.rect.y:
                    self.course = 1
                elif hero_y < self.rect.y:
                    self.course = 3

        #стрельба
        if self.isBullet == False :
            if 40 > random.randint (1, 1000):
                self.fire = 1

        self.config.counter -= 1 #уменьшаем счётчик цикла update
        self.impact = False