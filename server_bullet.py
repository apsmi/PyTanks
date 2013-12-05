# -*- coding: utf-8 -*-

from pygame import sprite, Rect

BUM_COUNT = 10

class Bullet(sprite.Sprite):
    def __init__(self, id, x, y, shutdirection):
        sprite.Sprite.__init__(self)

        self.MOVE_SPEED = 7
        self.BUM_WIDTH = 22
        self.BUM_HEIGHT = 22

        self.bum = 0    # индикатор взрыва пули
        self.xvel = 0   # скорость полета пули
        self.yvel = 0   # скорость полета пули
        self.startX = x # начальная позиция
        self.startY = y # начальная позиция
        self.WIDTH = 6  # ширина картинки
        self.HEIGHT = 6 # высота картинки

        self.id = id

        # определяем направление полета
        if shutdirection == "":
            self.shutdirection = "up"
        else:
            self.shutdirection = shutdirection

        # определяем положение пули
        if shutdirection == "left":
            self.startX -= 6
            self.startY += 11
        elif shutdirection == "right":
            self.startX += 28
            self.startY += 11
        elif shutdirection == "up":
            self.startX += 11
            self.startY += 6
        elif shutdirection == "down":
            self.startX += 11
            self.startY += 28

        self.rect = Rect(self.startX, self.startY, self.WIDTH, self.HEIGHT) # прямоугольный объект

    def update(self, obstructions):

        left = right = up = down = False

        if self.shutdirection == "left":
            left = True
        if self.shutdirection == "right":
            right = True
        if self.shutdirection == "up":
            up = True
        if self.shutdirection == "down":
            down = True
        if self.shutdirection == "stop":
            left = right = up = down = False

        if left:
            self.xvel = -self.MOVE_SPEED # Лево = x - n

        if right:
            self.xvel = self.MOVE_SPEED # Право = x + n

        if not(left or right): # стоим, когда нет указаний идти вправо-влево или попали куда-то
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, obstructions) #проверяем столкновения

        if up:
            self.yvel = -self.MOVE_SPEED # верх = x- n

        if down:
            self.yvel = self.MOVE_SPEED # низ = x + n

        if not(up or down): # стоим, когда нет указаний идти вправо - влево или попали куда-то
            self.yvel = 0

        self.rect.y += self.yvel # переносим свои положение на yvel
        self.collide(0, self.yvel, obstructions)#проверяем столкновения

        if (0 < self.bum):
            if (self.bum < BUM_COUNT):
                self.rect = Rect(self.rect.left, self.rect.top, self.BUM_WIDTH, self.BUM_HEIGHT) # прямоугольный объект
                self.bum += 1
            else:
                self.kill()
                self.shooter.isBullet = False # сообщаем тому, кто выстрелил, что его пуля кердык

    def collide(self, xvel, yvel, obstructions):

        for p in obstructions:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                #если пуля не начала взрываться, то начинаем взрывать ее
                if self.bum == 0:
                    self.rect.left -= 8
                    self.rect.top -= 8
                    self.bum = 1
                    p.die(self.shutdirection)   # сообщаем объекту, в который попали, что в него попали

                if xvel > 0:                      # если движется вправо
                    self.rect.right -= xvel # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left -= xvel # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom -= yvel # то не падает вниз

                if yvel < 0:                      # если движется вверх
                    self.rect.top -= yvel # то не движется вверх

                self.shutdirection = "stop"

    def die(self, shutdirection):
        return 0