# -*- coding: utf-8 -*-

from pygame import sprite, Rect
import pyganim



#TODO: change to kivy from image and Surface

class Tank_config():
    """
      Данный класс описывает конфигурацию танка. Содержит только те свойства, которые влияют на поведение танка.
    """
    def __init__(self):
        self.START_X = 34                         # начальные координаты по горизрнтали
        self.START_Y = 34                         # начальные координаты по вертикали
        self.MOVE_SPEED_X = 1                     # скорость перемещения по горизонтали
        self.MOVE_SPEED_Y = 1                     # скорость перемещения по вертикали
        self.WIDTH = 28                           # ширина аватарки
        self.HEIGHT = 28                          # высота автарки
        self.lifeStart = 1                        # количество жизней танка
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

    def __init__(self, config):
        sprite.Sprite.__init__(self)

        self.config = config

        self.course = ""                 # направление движения
        self.shutdirection = "up"           # направление выстрела
        self.isBullet = False               # флаг существования пули
        self.life = self.config.lifeStart   # оставшееся количество жизней
        self.xvel = 0                       # cкорость движения по горизонтали, 0 - стоит на месте
        self.yvel = 0                       # скорость движения по вертикали, 0 - не двигается
        self.dead = 0                       # счетчик кадров при смерти
        self.COLOR =  "#000000"             # цвет фона аватарки

        # автарка танка
        self.texture = Image("tanks/player1_1.png")#.texture
        #self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
        self.rect = Rect(self.config.START_X, self.config.START_Y, self.config.WIDTH, self.config.HEIGHT) # прямоугольный объект
        #self.image = image.load(self.config.INIT_IMAGE)

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

    def update(self,  obstructions):

        # если танк взорвали
        if (self.dead > 0):
            if (self.dead < 30):

                # показываем анимацию взрыва
                #self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                #self.image.fill(Color(self.COLOR))
                #self.image.set_colorkey(Color(self.COLOR))
                #self.boltAnimDie.blit(self.image, (0, 0))
                self.texture = Image(self.config.INIT_IMAGE).texture  # TODO: port anim to kivy
                self.dead += 1 # счетчик кадро анимации взрыва

            else:

                # закончили показывать взрыв, респауним танк
                self.rect.x = self.config.START_X
                self.rect.y = self.config.START_Y
                self.dead = 0
                #self.image = image.load(self.config.INIT_IMAGE)
                self.texture = Image(self.config.INIT_IMAGE).texture
                self.course = ""
                self.shutdirection = "up"

        # если танк не взорван, то двигаем танк в соответсвующем направлении
        else:

            # движение влево
            if self.course == "left":
                self.shutdirection = "left"                                  # изменяем направление выстрела
                self.xvel = -self.config.MOVE_SPEED_X                        # текущая скорость движения
                #self.image = Surface((self.config.WIDTH,self.config.HEIGHT)) # перерисовываем аватарку
                #self.image.fill(Color(self.COLOR))                           # заливаем фон
                #self.image.set_colorkey(Color(self.COLOR))                   # делаем фон прозрачным
                #self.boltAnimMove.blit(self.image, (0, 0))                   # выводим анимацию
                self.texture = Image(self.config.INIT_IMAGE).texture  # TODO: port anim to kivy
                #self.image = transform.rotate(self.image, 90)                # поворачиваем по направлению движения

            # движение вправо
            elif self.course == "right":
                self.shutdirection = "right"
                self.xvel = self.config.MOVE_SPEED_X
                #self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                #self.image.fill(Color(self.COLOR))
                #self.image.set_colorkey(Color(self.COLOR))
                self.texture = Image(self.config.INIT_IMAGE).texture  # TODO: port anim to kivy
                #self.boltAnimMove.blit(self.image, (0, 0))
                #self.image = transform.rotate(self.image, 270)

            # стоим, когда нет указаний идти вправо - влево
            else:
                self.xvel = 0

            self.rect.x += self.xvel                 # переносим свои положение на xvel
            self.collide(self.xvel, 0, obstructions) # проверяем столкновения

            # движение вверх
            if self.course == "up":
                self.shutdirection = "up"
                self.yvel = -self.config.MOVE_SPEED_Y
                #self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                #self.image.fill(Color(self.COLOR))
                #self.image.set_colorkey(Color(self.COLOR))
                #self.boltAnimMove.blit(self.image, (0, 0))
                self.texture = Image(self.config.INIT_IMAGE).texture  # TODO: port anim to kivy

            # движение вниз
            elif self.course == "down":
                self.shutdirection = "down"
                self.yvel = self.config.MOVE_SPEED_Y
                #self.image = Surface((self.config.WIDTH,self.config.HEIGHT))
                #self.image.fill(Color(self.COLOR))
                #self.image.set_colorkey(Color(self.COLOR))
                #self.boltAnimMove.blit(self.image, (0, 0))
                #self.image = transform.rotate(self.image, 180)
                self.texture = Image(self.config.INIT_IMAGE).texture  # TODO: port anim to kivy

            # стоим, когда нет указаний идти вверх - вниз
            else:
                self.yvel = 0

            self.rect.y += self.yvel                 # переносим свои положение на yvel
            self.collide(0, self.yvel, obstructions) # проверяем столкновения

    def collide(self, xvel, yvel, obstructions):

        # проверяем столкновения с препятствиями
        for p in obstructions:
            if p != self:

                if sprite.collide_rect(self, p): # если есть пересечение чего-то с танком

                    if xvel > 0:                 # если движется вправо
                        self.rect.right -= xvel  # то не движется вправо

                    if xvel < 0:                 # если движется влево
                        self.rect.left -= xvel   # то не движется влево

                    if yvel > 0:                 # если падает вниз
                        self.rect.bottom -= yvel # то не падает вниз

                    if yvel < 0:                 # если движется вверх
                        self.rect.top -= yvel    # то не движется вверх

    def die(self, shutdirection):

        # умираем, если попадает пуля
        # если попадание последнее
        if self.life == 1:

            # начинаем взрыывать танк
            self.dead = 1
            self.life = self.config.lifeStart

        # если жизни еще есть
        else:

            # то их стало меньше
            self.life -= 1