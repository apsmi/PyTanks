# -*- coding: utf-8 -*-

import random

from tank import TankWidget
from bullet import Bullet

from kivy.core.image import Image
from kivy.graphics import Rectangle


class MonsterWidget(TankWidget):
    def __init__(self):
        TankWidget.__init__(self)

        self.fire = 0   # выстрел
        self.impact = False  # переменная столкновения
        self.counterStart = 78  # счётчик поиска игрока (сложность)
        self.counter = self.counterStart

    def update(self, obstructions, hero_y, hero_x, monsters_bullets, anim, canvas):  # по принципу героя

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 15):

                if anim:
                    self.rectangle.texture = self.t_b_2   # TODO: подумать над тем, как не присваивать каждый раз
                else:
                    self.rectangle.texture = self.t_b_3
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                x = random.randint(40, 600)
                y = random.randint(40, 400)
                self.pos = (x, y)

                self.dead = 0
                self.rectangle.texture = self.t_u_1

        else:

            #наведение на героя
            if self.counter == 0:
                if 50 < random.randint(1, 100) and hero_y != self.y:
                    if self.impact is False:
                        if hero_y > self.y:
                            self.course = "up"
                        elif hero_y < self.y:
                            self.course = "down"
                else:
                    if self.impact is False:
                        if hero_x > self.x:
                            self.course = "right"
                        elif hero_x < self.x:
                            self.course = "left"
                self.counter = self.counterStart

            #проверка на макс. пройденое расстояние
            if (self.START_X - self.x) > self.maxLengthLeft:
                self.course = "right"
                self.counter = 200  # включаем дурака
            if (self.START_Y - self.y) > self.maxLengthUp:
                self.course = "up"
                self.counter = 20  # включаем дурака
            if (self.START_X - self.x) < 0 and (self.x - self.START_X) > self.maxLengthLeft:
                self.course = "left"
                self.counter = 20  # включаем дурака
            if (self.START_Y - self.y) < 0 and (self.y - self.START_Y) > self.maxLengthUp:
                self.course = "down"
                self.counter = 20  # включаем дурака

            #course - направление
            #обнуляем движение
            xvel = yvel = 0

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                xvel = -self.MOVE_SPEED_X                        # текущая скорость движения

                if anim:
                    self.rectangle.texture = self.t_l_1
                else:
                    self.rectangle.texture = self.t_l_2

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                xvel = self.MOVE_SPEED_X

                if anim:
                    self.rectangle.texture = self.t_r_1
                else:
                    self.rectangle.texture = self.t_r_2

            # движение вверх
            elif self.course == "up":
                self.shutdirection = "up"
                yvel = self.MOVE_SPEED_Y

                if anim:
                    self.rectangle.texture = self.t_u_1
                else:
                    self.rectangle.texture = self.t_u_2

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                yvel = -self.MOVE_SPEED_Y

                if anim:
                    self.rectangle.texture = self.t_d_1
                else:
                    self.rectangle.texture = self.t_d_2

            self.pos[0] += xvel                 # переносим свои положение на xvel
            self.pos[1] += yvel                 # переносим свои положение на yvel

            self.collide(xvel, yvel, obstructions)  # проверяем столкновения

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


class Monster1(MonsterWidget):
    def __init__(self):
        MonsterWidget.__init__(self)

        self.t_u_1 = Image('tanks/monster1_u_1.png').texture
        self.t_u_2 = Image('tanks/monster1_u_2.png').texture
        self.t_r_1 = Image('tanks/monster1_r_1.png').texture
        self.t_r_2 = Image('tanks/monster1_r_2.png').texture
        self.t_d_1 = Image('tanks/monster1_d_1.png').texture
        self.t_d_2 = Image('tanks/monster1_d_2.png').texture
        self.t_l_1 = Image('tanks/monster1_l_1.png').texture
        self.t_l_2 = Image('tanks/monster1_l_2.png').texture

        self.maxLengthLeft = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 3  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 3  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 78  # счётчик поиска игрока (сложность)


class Monster2(MonsterWidget):
    def __init__(self,):
        MonsterWidget.__init__(self)

        self.t_u_1 = Image('tanks/monster2_u_1.png').texture
        self.t_u_2 = Image('tanks/monster2_u_2.png').texture
        self.t_r_1 = Image('tanks/monster2_r_1.png').texture
        self.t_r_2 = Image('tanks/monster2_r_2.png').texture
        self.t_d_1 = Image('tanks/monster2_d_1.png').texture
        self.t_d_2 = Image('tanks/monster2_d_2.png').texture
        self.t_l_1 = Image('tanks/monster2_l_1.png').texture
        self.t_l_2 = Image('tanks/monster2_l_2.png').texture

        self.maxLengthLeft = 300  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 300  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 2  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 2  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 20  # счётчик поиска игрока (сложность)


class Monster3(MonsterWidget):
    def __init__(self):
        MonsterWidget.__init__(self)

        self.t_u_1 = Image('tanks/monster3_u_1.png').texture
        self.t_u_2 = Image('tanks/monster3_u_2.png').texture
        self.t_r_1 = Image('tanks/monster3_r_1.png').texture
        self.t_r_2 = Image('tanks/monster3_r_2.png').texture
        self.t_d_1 = Image('tanks/monster3_d_1.png').texture
        self.t_d_2 = Image('tanks/monster3_d_2.png').texture
        self.t_l_1 = Image('tanks/monster3_l_1.png').texture
        self.t_l_2 = Image('tanks/monster3_l_2.png').texture

        self.maxLengthLeft = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 56  # счётчик поиска игрока (сложность)

        self.lifeStart = 3