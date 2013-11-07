# -*- coding: utf-8 -*-

import random
from pygame import *
from tank import Tank
from bullet import Bullet

class Monster(Tank):
    def __init__(self, config):
        Tank.__init__(self, config)

        self.fire = 0   # выстрел
        self.impact = False # переменная столкновения
        self.counter = self.config.counterStart

    def update(self, obstructions, hero_y, hero_x, monsters_bullets): # по принципу героя

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 30):

                # показываем анимацию взрыва
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR))
                self.boltAnimDie.blit(self.image, (0, 0))
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = self.config.START_X
                self.rect.y = self.config.START_Y
                self.dead = 0
                self.image = image.load(self.config.INIT_IMAGE)

        else:

            #наведение на героя
            if self.counter == 0:
                if 50 < random.randint (1,100) and hero_y != self.rect.y:
                    if self.impact == False:
                        if hero_y > self.rect.y:
                            self.course = "down"
                        elif hero_y < self.rect.y:
                            self.course = "up"
                else:
                    if self.impact == False:
                        if hero_x > self.rect.x:
                            self.course = "right"
                        elif hero_x < self.rect.x:
                            self.course = "left"
                self.counter = self.config.counterStart


            #проверка на макс. пройденое расстояние
            if (abs(self.config.START_X - self.rect.x) > self.config.maxLengthLeft):
                self.course = "right"
                self.counter = 200 # включаем дурака
                #self.config.xvel =-self.config.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
            if (abs(self.config.START_Y - self.rect.y) > self.config.maxLengthUp):
                self.course = "down"
                self.counter = 200 # включаем дурака
                #self.config.yvel = -self.config.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль
# TODO: дописать еще два направления


            #course - направление
            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED_X                        # текущая скорость движения
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT)) # перерисовываем аватарку
                self.image.fill(Color(self.COLOR))                           # заливаем фон
                self.image.set_colorkey(Color(self.COLOR))                   # делаем фон прозрачным
                self.boltAnimMove.blit(self.image, (0, 0))                   # выводим анимацию
                self.image = transform.rotate(self.image, 90)                # поворачиваем по направлению движения

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR))
                self.boltAnimMove.blit(self.image, (0, 0))
                self.image = transform.rotate(self.image, 270)

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = -self.config.MOVE_SPEED_Y
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR))
                self.boltAnimMove.blit(self.image, (0, 0))

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = self.config.MOVE_SPEED_Y
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR))
                self.boltAnimMove.blit(self.image, (0, 0))
                self.image = transform.rotate(self.image, 180)

            # стоим, когда нет указаний идти вверх - вниз
            else:
                self.yvel = 0

            self.rect.y += self.yvel                 # переносим свои положение на yvel
            self.collide(0, self.yvel, obstructions) # проверяем столкновения


            # если упердись в препятствие - повернулись
            if self.impact == True:
                if hero_y == self.rect.y:
                    if hero_x > self.rect.x:
                        self.course = "right"
                    elif hero_x < self.rect.x:
                        self.course = "left"

                if hero_x == self.rect.x:
                    if hero_y > self.rect.y:
                        self.course = "down"
                    elif hero_y < self.rect.y:
                        self.course = "up"

            #стрельба
            if self.isBullet == False :
                if 40 > random.randint (1, 1000):
                    bullet = Bullet(self.rect.x,self.rect.y,self.shutdirection)
                    bullet.shooter = self
                    monsters_bullets.add(bullet)
                    self.isBullet = True

            self.counter -= 1 #уменьшаем счётчик цикла update
            self.impact = False