# -*- coding: utf-8 -*-

import random

from tank import Tank
from bullet import Bullet

from kivy.graphics import Rectangle


class Monster(Tank):
    def __init__(self, config):
        Tank.__init__(self, config)

        self.fire = 0   # выстрел
        self.impact = False  # переменная столкновения
        self.counter = self.config.counterStart

    def update(self, obstructions, hero_y, hero_x, monsters_bullets, anim, canvas):  # по принципу героя

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 15):

                if anim:
                    self.texture = self.config.t_b_2
                else:
                    self.texture = self.config.t_b_3
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = random.randint(40, 600)
                self.rect.y = random.randint(40, 400)
                self.dead = 0
                self.texture = self.config.t_u_1

        else:

            #наведение на героя
            if self.counter == 0:
                if 50 < random.randint (1,100) and hero_y != self.rect.y:
                    if self.impact is False:
                        if hero_y > self.rect.y:
                            self.course = "up"
                        elif hero_y < self.rect.y:
                            self.course = "down"
                else:
                    if self.impact is False:
                        if hero_x > self.rect.x:
                            self.course = "right"
                        elif hero_x < self.rect.x:
                            self.course = "left"
                self.counter = self.config.counterStart

            #проверка на макс. пройденое расстояние
            if (self.config.START_X - self.rect.x) > self.config.maxLengthLeft:
                self.course = "right"
                self.counter = 200  # включаем дурака
            if (self.config.START_Y - self.rect.y) > self.config.maxLengthUp:
                self.course = "up"
                self.counter = 20  # включаем дурака
            if (self.config.START_X - self.rect.x) < 0 and (self.rect.x - self.config.START_X) > self.config.maxLengthLeft:
                self.course = "left"
                self.counter = 20  # включаем дурака
            if (self.config.START_Y - self.rect.y) < 0 and (self.rect.y - self.config.START_Y) > self.config.maxLengthUp:
                self.course = "down"
                self.counter = 20  # включаем дурака

            #course - направление
            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED_X                        # текущая скорость движения
                if anim:
                    self.texture = self.config.t_l_1
                else:
                    self.texture = self.config.t_l_2

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X
                if anim:
                    self.texture = self.config.t_r_1
                else:
                    self.texture = self.config.t_r_2

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = self.config.MOVE_SPEED_Y
                if anim:
                    self.texture = self.config.t_u_1
                else:
                    self.texture = self.config.t_u_2

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = -self.config.MOVE_SPEED_Y
                if anim:
                    self.texture = self.config.t_d_1
                else:
                    self.texture = self.config.t_d_2

            # стоим, когда нет указаний идти вверх - вниз
            else:
                self.yvel = 0

            self.rect.y += self.yvel                 # переносим свои положение на yvel
            self.collide(0, self.yvel, obstructions)  # проверяем столкновения


            # если упердись в препятствие - повернулись
            if self.impact is True:
                if hero_y == self.rect.y:
                    if hero_x > self.rect.x:
                        self.course = "right"
                    elif hero_x < self.rect.x:
                        self.course = "left"

                if hero_x == self.rect.x:
                    if hero_y > self.rect.y:
                        self.course = "up"
                    elif hero_y < self.rect.y:
                        self.course = "down"

            #стрельба
            if self.isBullet is False:
                if 40 > random.randint(1, 1000):
                    bullet = Bullet(self.rect.x, self.rect.y, self.shutdirection)
                    bullet.shooter = self
                    with canvas:
                        bullet.picture = Rectangle(texture=bullet.texture,
                                                   pos=(bullet.rect.x, bullet.rect.y),
                                                   size=bullet.texture.size)
                    monsters_bullets.add(bullet)
                    self.isBullet = True

            self.counter -= 1  # уменьшаем счётчик цикла update
            self.impact = False