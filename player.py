# -*- coding: utf-8 -*-

from pygame import *
from tank import Tank

class Player(Tank):
    def update(self,  platforms):
        if (self.dead > 0):
            if (self.dead < 30):
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.config.COLOR))
                self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
                self.boltAnimDie.blit(self.image, (0, 0))  #animation
                self.dead += 1
            else:
                self.rect.x = self.startX
                self.rect.y = self.startY
                self.dead = 0
                self.image = image.load(self.config.INIT_IMAGE)
                self.direction = ""
                self.shutdirection = "up"
        else:
            if self.direction == "left":
                self.shutdirection = "left"
                self.xvel = -self.config.MOVE_SPEED_X # Лево = x- n
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.config.COLOR))
                self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
                self.boltAnimLeft.blit(self.image, (0, 0))  #animation
                self.image = transform.rotate(self.image, 90)
            elif self.direction == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X # Право = x + n
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.config.COLOR))
                self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
                self.boltAnimRight.blit(self.image, (0, 0))#animation
                self.image = transform.rotate(self.image, 270)
            else: # стоим, когда нет указаний идти вправо - влево
                self.xvel = 0

            self.rect.x += self.xvel # переносим свои положение на xvel
            self.collide(self.xvel, 0, platforms) #проверяем столкновения

            if self.direction == "up":
                self.shutdirection = "up"
                self.yvel = -self.config.MOVE_SPEED_Y # верх = x- n
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.config.COLOR))
                self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
                self.boltAnimUp.blit(self.image, (0, 0))#animation
            elif self.direction == "down":
                self.shutdirection = "down"
                self.yvel = self.config.MOVE_SPEED_Y # низ = x + n
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.config.COLOR))
                self.image.set_colorkey(Color(self.config.COLOR)) # делаем фон прозрачным
                self.boltAnimDown.blit(self.image, (0, 0))#animation
                self.image = transform.rotate(self.image, 180)
            else: # стоим, когда нет указаний идти вправо - влево
                self.yvel = 0

            self.rect.y += self.yvel # переносим свои положение на yvel
            self.collide(0, self.yvel, platforms)#проверяем столкновения