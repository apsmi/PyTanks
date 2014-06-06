# -*- coding: utf-8 -*-

from pygame import sprite, font, Surface, Rect, image, Color, transform
import pyganim

class Tank_config():
    """
      Данный класс описывает конфигурацию танка. Содержит только те свойства, которые влияют на поведение танка.
    """
    def __init__(self, x, y, DEAD_COUNT):
        self.DEAD_COUNT = DEAD_COUNT
        self.START_X = x                         # начальные координаты по горизрнтали
        self.START_Y = y                         # начальные координаты по вертикали
        self.WIDTH = 28                           # ширина аватарки
        self.HEIGHT = 28                          # высота автарки
        self.ANIMATION_DELAY = 0.1                # скорость анимации аватарки
        self.ANIMATION =     ['tanks/player1_1.png', # анимация при движении
                              'tanks/player1_2.png']
        self.ANIMATION_DIE = ['tanks/die_1.png',  # анимация при взрыве
                              'tanks/die_2.png',
                              'tanks/die_3.png']
        self.INIT_IMAGE =     "tanks/player1_1.png"  # изображение при появлении танка


class Tank(sprite.Sprite):
    """
        Это основной класс, реализующий поведение танка.
    """

    def __init__(self, config, id, team):
        sprite.Sprite.__init__(self)

        self.config = config
        self.id = id
        self.team = team
        self.name = ""

        self.course = ""                 # направление движения
        self.shutdirection = "up"           # направление выстрела
        self.dead = 0                       # счетчик кадров при смерти
        self.COLOR =  "#000000"             # цвет фона аватарки

        # надпись
        #font_obj = font.Font('freesansbold.ttf', 12)
        #if team == "green":
            #self.label = font_obj.render(id, True, Color("green"))
        #else:
            #self.label = font_obj.render(id, True, Color("yellow"))

        # автарка танка
        self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
        self.rect = Rect(self.config.START_X, self.config.START_Y, self.config.WIDTH, self.config.HEIGHT) # прямоугольный объект
        self.image = image.load(self.config.INIT_IMAGE)

        #  Анимация движения
        boltAnim = []
        for anim in self.config.ANIMATION:
            boltAnim.append((anim, self.config.ANIMATION_DELAY))
        self.boltAnimMove = pyganim.PygAnimation(boltAnim)
        self.boltAnimMove.play()

        # Анимация уничтожения
        boltAnim = []
        for anim in self.config.ANIMATION_DIE:
            boltAnim.append((anim, 0.2))
        self.boltAnimDie = pyganim.PygAnimation(boltAnim)
        self.boltAnimDie.play()

    def update(self, x, y, course, shutdirection, dead):

        self.rect.x, self.rect.y, self.course, self.shutdirection, self.dead = x, y, course, shutdirection, dead

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < self.config.DEAD_COUNT):

                # показываем анимацию взрыва
                self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                self.image.fill(Color(self.COLOR))
                self.image.set_colorkey(Color(self.COLOR))
                self.boltAnimDie.blit(self.image, (0, 0))

            else:

                # закончили показывать взрыв, респауним танк
                self.image = image.load(self.config.INIT_IMAGE)
                #  Анимация движения
                boltAnim = []
                for anim in self.config.ANIMATION:
                    boltAnim.append((anim, self.config.ANIMATION_DELAY))
                self.boltAnimMove = pyganim.PygAnimation(boltAnim)
                self.boltAnimMove.play()

        # направление
        else:

            self.image = Surface((self.config.WIDTH,self.config.HEIGHT)) # перерисовываем аватарку
            self.image.fill(Color(self.COLOR))                           # заливаем фон
            self.image.set_colorkey(Color(self.COLOR))                   # делаем фон прозрачным
            self.boltAnimMove.blit(self.image, (0, 0))                   # выводим анимацию

            # движение влево
            if self.shutdirection == "left":
                self.image = transform.rotate(self.image, 90)                # поворачиваем по направлению движения

            # движение вправо
            elif self.shutdirection == "right":
                self.image = transform.rotate(self.image, 270)

            # движение вниз
            elif self.shutdirection == "down":
                self.image = transform.rotate(self.image, 180)