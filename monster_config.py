__author__ = 'cam'

from tank import Tank_config

class Monster_config_1 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)
        self.START_X = START_X
        self.START_Y = START_Y
        self.ANIMATION_RIGHT = ['tanks\m_a_right_1.png',
                           'tanks\m_a_right_2.png']
        self.ANIMATION_LEFT = ['tanks\m_a_left_1.png',
                          'tanks\m_a_left_2.png']

        self.ANIMATION_UP = ['tanks\m_a_up_1.png',
                        'tanks\m_a_up_2.png']
        self.ANIMATION_DOWN = ['tanks\m_a_down_1.png',
                          'tanks\m_a_down_2.png']
        self.INIT_IMAGE = "tanks\m_a_up_1.png"

        self.maxLengthLeft = 300 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 300 # макс. пройденое расстояние от точки спавна

        self.xvel = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 1 # скорость движения по вертикали, 0 - не двигается

        self.counter = 20 # счётчик поиска игрока (сложность)

class Monster_config_2 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)
        self.START_X = START_X
        self.START_Y = START_Y
        self.ANIMATION_RIGHT = ['tanks\m_a_right_1.png',
                           'tanks\m_a_right_2.png']
        self.ANIMATION_LEFT = ['tanks\m_a_left_1.png',
                          'tanks\m_a_left_2.png']

        self.ANIMATION_UP = ['tanks\m_a_up_1.png',
                        'tanks\m_a_up_2.png']
        self.ANIMATION_DOWN = ['tanks\m_a_down_1.png',
                          'tanks\m_a_down_2.png']
        self.INIT_IMAGE = "tanks\m_a_up_1.png"

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна

        self.xvel = 2 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 2 # скорость движения по вертикали, 0 - не двигается

        self.counter = 30 # счётчик поиска игрока (сложность)

class Monster_config_3 (Tank_config):
    def __init__(self, START_X, START_Y):
        Tank_config.__init__(self)
        self.START_X = START_X
        self.START_Y = START_Y
        self.ANIMATION_RIGHT = ['tanks\m_a_right_1.png',
                           'tanks\m_a_right_2.png']
        self.ANIMATION_LEFT = ['tanks\m_a_left_1.png',
                          'tanks\m_a_left_2.png']

        self.ANIMATION_UP = ['tanks\m_a_up_1.png',
                        'tanks\m_a_up_2.png']
        self.ANIMATION_DOWN = ['tanks\m_a_down_1.png',
                          'tanks\m_a_down_2.png']
        self.INIT_IMAGE = "tanks\m_a_up_1.png"

        self.maxLengthLeft = 500 # макс. пройденое расстояние от точки спавна
        self.maxLengthUp = 500 # макс. пройденое расстояние от точки спавна

        self.xvel = 1 # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = 1 # скорость движения по вертикали, 0 - не двигается

        self.counter = 25 # счётчик поиска игрока (сложность)

        self.life = 3 # счётчик жизней
        self.lifeStart = self.life