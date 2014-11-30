# -*- coding: utf-8 -*-

import random

from tank import TankWidget
from bullet import Bullet

from kivy.core.image import Image
from kivy.graphics import Rectangle


class MonsterWidget(TankWidget):
    def __init__(self):
        TankWidget.__init__(self)

        # индивидуально, задано в конфиге
        self.counterStart = 78  # счётчик поиска игрока (сложность)
        self.maxLengthLeft = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        # для всех монстров
        self.fire = 0   # выстрел
        self.impact = False  # переменная столкновения
        self.counter = 0

    def update(self, obstructions, hero_y, hero_x, anim):  # по принципу героя

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 15):

                if anim:
                    self.rectangle.texture = self.t_b_2
                else:
                    self.rectangle.texture = self.t_b_3
                self.dead += 1  # счетчик кадров анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.START_X = random.randint(40, 600)
                self.START_Y = random.randint(40, 400)
                self.pos = (self.START_X, self.START_Y)

                self.dead = 0
                self.rectangle.texture = self.t_u_1
                self.course = ""
                self.shutdirection = "up"

                self.parent.monsters.append(self)  # включаем танк в массив танков

        else:

            # наведение на героя
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

            # проверка на макс. пройденое расстояние
            if (self.START_X - self.x) > self.maxLengthLeft:
                self.course = "right"
                self.counter = 20  # включаем дурака
            if (self.START_Y - self.y) > self.maxLengthUp:
                self.course = "up"
                self.counter = 20  # включаем дурака
            if (self.START_X - self.x) < 0 and (self.x - self.START_X) > self.maxLengthLeft:
                self.course = "left"
                self.counter = 20  # включаем дурака
            if (self.START_Y - self.y) < 0 and (self.y - self.START_Y) > self.maxLengthUp:
                self.course = "down"
                self.counter = 20  # включаем дурака

            # course - направление
            # обнуляем движение
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

            self.x += xvel                 # переносим свои положение на xvel
            self.y += yvel                 # переносим свои положение на yvel

            self.impact = self.collide(xvel, yvel, obstructions)  # проверяем столкновения

            # если упердись в препятствие - повернулись
            if self.impact is True:
                if self.course == "down" or self.course == "up":
                    if hero_x > self.x:
                        self.course = "right"
                    elif hero_x < self.x:
                        self.course = "left"

                if self.course == "left" or self.course == "right":
                    if hero_y > self.y:
                        self.course = "up"
                    elif hero_y < self.y:
                        self.course = "down"

            # стрельба

            # если у стреляющего нет пули, то стреляем
            if self.isBullet is False:
                if 40 > random.randint(1, 1000):

                    # создаем виджет пули
                    bullet = Bullet(self.x, self.y, self.shutdirection)

                    # говорим пуле чья она
                    bullet.shooter = self

                    # добавляем виджет пули на основное окно
                    self.parent.add_widget(bullet)

                    # добавляем пулю в массив пуль монстров
                    bullet.list = self.parent.monsters_bullets
                    self.parent.monsters_bullets.append(bullet)

                    # флаг существования пули у выстрелившего монстра
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

        with self.canvas:
            self.rectangle = Rectangle(texture=self.t_u_1, size=self.t_u_1.size)

        self.maxLengthLeft = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 3  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 3  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 78  # счётчик поиска игрока (сложность)

        self.life = self.lifeStart   # оставшееся количество жизней


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

        with self.canvas:
            self.rectangle = Rectangle(texture=self.t_u_1, size=self.t_u_1.size)

        self.maxLengthLeft = 300  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 300  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 2  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 2  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 20  # счётчик поиска игрока (сложность)

        self.life = self.lifeStart   # оставшееся количество жизней


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

        with self.canvas:
            self.rectangle = Rectangle(texture=self.t_u_1, size=self.t_u_1.size)

        self.maxLengthLeft = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500  # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500  # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1  # скорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1  # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 56  # счётчик поиска игрока (сложность)

        self.lifeStart = 3
        self.life = self.lifeStart   # оставшееся количество жизней