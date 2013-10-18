# -*- coding: utf-8 -*-

from pygame import *
from tank import Tank


class Player(Tank):
    def update(self,  left, right, up, down, platforms):
        if left:
            self.xvel = -self.config.MOVE_SPEED_X # Лево = x- n
            self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
            self.image.fill(Color(self.config.COLOR))
            self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
            self.boltAnimLeft.blit(self.image, (0, 0))  #animation
            self.image = transform.rotate(self.image, 90)

        if right:
            self.xvel = self.config.MOVE_SPEED_X # Право = x + n
            self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
            self.image.fill(Color(self.config.COLOR))
            self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
            self.boltAnimRight.blit(self.image, (0, 0))#animation
            self.image = transform.rotate(self.image, 270)

        if not(left or right): # стоим, когда нет указаний идти вправо - влево
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms) #проверяем столкновения

        if up:
            self.yvel = -self.config.MOVE_SPEED_Y # верх = x- n
            self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
            self.image.fill(Color(self.config.COLOR))
            self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
            self.boltAnimUp.blit(self.image, (0, 0))#animation

        if down:
            self.yvel = self.config.MOVE_SPEED_Y # низ = x + n
            self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
            self.image.fill(Color(self.config.COLOR))
            self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
            self.boltAnimDown.blit(self.image, (0, 0))#animation
            self.image = transform.rotate(self.image, 180)

        if not(up or down): # стоим, когда нет указаний идти вправо - влево
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, platforms)#проверяем столкновения