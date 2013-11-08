# -*- coding: utf-8 -*-

from tank import Tank_config

class Monster_config_1 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)

        self.START_X = START_X
        self.START_Y = START_Y

        self.ANIMATION = ['tanks\monster1_1.png',
                        'tanks\monster1_2.png',
                        'tanks\monster1_3.png']
        self.INIT_IMAGE = "tanks\monster1_1.png"

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 2 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 2 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 78 # счётчик поиска игрока (сложность)

class Monster_config_2 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)
        self.START_X = START_X
        self.START_Y = START_Y

        self.ANIMATION = ['tanks\monster2_1.png',
                        'tanks\monster2_2.png']
        self.INIT_IMAGE = "tanks\monster2_1.png"

        self.maxLengthLeft = 300 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 300 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 20 # счётчик поиска игрока (сложность)

class Monster_config_3 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)
        self.START_X = START_X
        self.START_Y = START_Y

        self.ANIMATION = ['tanks\monster3_1.png',
                           'tanks\monster3_2.png']
        self.INIT_IMAGE = "tanks\monster3_1.png"

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthRight = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthDown = 500 # макс. пройденое расстояние от точки спавна

        self.MOVE_SPEED_X = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.MOVE_SPEED_Y = 1 # скорость движения по вертикали, 0 - не двигается

        self.counterStart = 56 # счётчик поиска игрока (сложность)

        self.lifeStart = 3
