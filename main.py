#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import Player
from blocks import Platform
from level import gen_level
from bullet import Bullet
from monster import Monster

#Объявляем переменные
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("PyTanks") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    hero = Player(34,34) # создаем героя по (x,y) координатам
    up = down = left = right = False    # по умолчанию — стоим

    entities = pygame.sprite.Group() # Все объекты
    monsters = pygame.sprite.Group() # Все передвигающиеся объекты
    platforms = [] # то, во что мы будем врезаться или опираться

    entities.add(hero)
    #platforms.append(hero)

    #2 координаты появления, скорость перемещения по горизонтали, скорость перемещения по вертикали, максимальное расстояние в одну сторону, которое может пройти монстр, по вертикали
    mn = Monster(736,580,1,1,20000,20000)
    entities.add(mn)
    #platforms.append(mn)
    monsters.add(mn)

    level = gen_level (20,25)

    #рисуем платформы
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-" or col == "*":
                pf = Platform(x,y,col)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    timer = pygame.time.Clock()

    isBullet = False
    shutdirection = "up"

    while 1: # Основной цикл программы

        timer.tick(60)

        for e in pygame.event.get(): # Обрабатываем события
            #выход
            if e.type == QUIT:
                raise SystemExit

            if e.type == KEYDOWN:

                if e.key == K_LEFT:
                    shutdirection = "left"

                    left = True
                    right = up = down = False

                elif e.key == K_RIGHT:
                    shutdirection = "right"

                    right = True
                    left = up = down = False

                elif e.key == K_UP:
                    shutdirection = "up"

                    up = True
                    left = right = down = False

                elif e.key == K_DOWN:
                    shutdirection = "down"

                    down = True
                    left = right = up = False

                if e.key == K_SPACE and not isBullet:
                    bullet = Bullet(hero.rect.left,hero.rect.top,shutdirection)
                    entities.add(bullet)
                    isBullet = True

            if e.type == KEYUP:
                if e.key == K_RIGHT:
                    right = False
                elif e.key == K_LEFT:
                    left = False
                elif e.key == K_UP:
                    up = False
                elif e.key == K_DOWN:
                    down = False

        if mn.fire == 1 and not mn.isBullet:
            bullet_mn = Bullet(mn.rect.x,mn.rect.y,mn.shutdirection)
            entities.add(bullet_mn)
            mn.isBullet = True

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать

        if isBullet:
            bullet.update(platforms+ [mn])
            if bullet.bum >= 20:
                entities.remove(bullet)
                bullet = None
                isBullet = False

        if mn.isBullet:
            bullet_mn.update(platforms + [hero])
            if bullet_mn.bum >= 20:
                entities.remove(bullet_mn)
                bullet_mn = None
                mn.isBullet = False

        hero.update(left, right, up, down, platforms + [mn]) # передвижение

        monsters.update(platforms + [hero] ) # передвигаем всех монстров

        entities.draw(screen) # отображение всего

        pygame.display.update()     # обновление и вывод всех изменений на экран

        for p in platforms:
            if (p.rect.width == 0) or (p.rect.height == 0):
                platforms.remove(p)

if __name__ == "__main__":
    main()
