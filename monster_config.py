# -*- coding: utf-8 -*-

from kivy.core.image import Image
import random

from tank import Tank_config


class Monster_config_1(Tank_config):
    def __init__(self):
        Tank_config.__init__(self)

        self.START_X = random.randint(1, 600)
        self.START_Y = random.randint(1, 400)

        self.t_u_1 = Image('tanks/monster1_u_1.png').texture
        self.t_u_2 = Image('tanks/monster1_u_2.png').texture
        self.t_r_1 = Image('tanks/monster1_r_1.png').texture
        self.t_r_2 = Image('tanks/monster1_r_2.png').texture
        self.t_d_1 = Image('tanks/monster1_d_1.png').texture
        self.t_d_2 = Image('tanks/monster1_d_2.png').texture
        self.t_l_1 = Image('tanks/monster1_l_1.png').texture
        self.t_l_2 = Image('tanks/monster1_l_2.png').texture

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 2 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 2 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 78 # счётчик поиска игрока (сложность)


class Monster_config_2(Tank_config):

    def __init__(self,):
        Tank_config.__init__(self)

        self.START_X = random.randint(1, 600)
        self.START_Y = random.randint(1, 400)

        self.t_u_1 = Image('tanks/monster2_u_1.png').texture
        self.t_u_2 = Image('tanks/monster2_u_2.png').texture
        self.t_r_1 = Image('tanks/monster2_r_1.png').texture
        self.t_r_2 = Image('tanks/monster2_r_2.png').texture
        self.t_d_1 = Image('tanks/monster2_d_1.png').texture
        self.t_d_2 = Image('tanks/monster2_d_2.png').texture
        self.t_l_1 = Image('tanks/monster2_l_1.png').texture
        self.t_l_2 = Image('tanks/monster2_l_2.png').texture

        self.maxLengthLeft = 300 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 300 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 20 # счётчик поиска игрока (сложность)


class Monster_config_3(Tank_config):
    def __init__(self):
        Tank_config.__init__(self)

        self.START_X = random.randint(1, 600)
        self.START_Y = random.randint(1, 400)

        self.t_u_1 = Image('tanks/monster3_u_1.png').texture
        self.t_u_2 = Image('tanks/monster3_u_2.png').texture
        self.t_r_1 = Image('tanks/monster3_r_1.png').texture
        self.t_r_2 = Image('tanks/monster3_r_2.png').texture
        self.t_d_1 = Image('tanks/monster3_d_1.png').texture
        self.t_d_2 = Image('tanks/monster3_d_2.png').texture
        self.t_l_1 = Image('tanks/monster3_l_1.png').texture
        self.t_l_2 = Image('tanks/monster3_l_2.png').texture

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 56 # счётчик поиска игрока (сложность)

        self.lifeStart = 3
