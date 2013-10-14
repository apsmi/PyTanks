#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from pygame import *
from player import Player
from blocks import Platform

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

    hero = Player(55,55) # создаем героя по (x,y) координатам
    up = down = left = right = False    # по умолчанию — стоим

    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    entities.add(hero)

    level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "-                       -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-                       -",
       "-                       -",
       "-      ---              -",
       "-                       -",
       "-   -----------         -",
       "-                       -",
       "-                -      -",
       "-                   --  -",
       "-                       -",
       "-                       -",
       "-------------------------"]

    #рисуем платформы
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    timer = pygame.time.Clock()

    while 1: # Основной цикл программы

        timer.tick(60)

        for e in pygame.event.get(): # Обрабатываем события
            #выход
            if e.type == QUIT:
                raise SystemExit

            if e.type == KEYDOWN and not (left or right or up or down):
                if e.key == K_LEFT:
                    left = True
                elif e.key == K_RIGHT:
                    right = True
                elif e.key == K_UP:
                    up = True
                elif e.key == K_DOWN:
                    down = True

            if e.type == KEYUP:
                if e.key == K_RIGHT:
                    right = False
                elif e.key == K_LEFT:
                    left = False
                elif e.key == K_UP:
                    up = False
                elif e.key == K_DOWN:
                    down = False

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать

        hero.update(left, right, up, down, platforms) # передвижение
        entities.draw(screen) # отображение всего

        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
