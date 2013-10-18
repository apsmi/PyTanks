#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import sys
from pygame import *
from player import Player
from blocks import Platform, PLATFORM_HEIGHT, PLATFORM_WIDTH
from level import gen_level
from bullet import Bullet
from monster import Monster
from tank import Tank_config
from monster_config import *

def window_init(width, height, color, caption):
    #инициализация окна
    display = (width, height) # Группируем ширину и высоту в одну переменную
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(display) # Создаем окошко
    pygame.display.set_caption(caption) # Пишем в шапку
    bg = Surface((width,height)) # Создание видимой поверхности, будем использовать как фон
    bg.fill(Color(color))     # Заливаем поверхность сплошным цветом
    return bg, screen

def main():
    #инициализация
    bg, screen = window_init(800, 640, "#000000", "PyTanks")

    #группы объектов
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться

    #создаем героя
    #hero = Player(34,34) # создаем героя по (x,y) координатам
    hero_config = Tank_config()
    hero = Player(hero_config)
    entities.add(hero) # добавляем героя во все объекты
    up = down = left = right = False    # по умолчанию — стоим

    #2 координаты появления, скорость перемещения по горизонтали, скорость перемещения по вертикали, максимальное расстояние в одну сторону, которое может пройти монстр, по вертикали
    mn_config = Monster_config_3(736,580)
    mn = Monster(mn_config)
    entities.add(mn)

    #генерируем уровень
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

    #таймер
    timer = pygame.time.Clock()

    hero.isBullet = False
    hero.shutdirection = "up"

    while 1: # Основной цикл программы

        timer.tick(60)#таймер на 60 кадров

        for e in pygame.event.get(): # Обрабатываем события
            #выход
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #действия героя
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    hero.shutdirection = "left"
                    left = True
                    right = up = down = False

                elif e.key == K_RIGHT:
                    hero.shutdirection = "right"
                    right = True
                    left = up = down = False

                elif e.key == K_UP:
                    hero.shutdirection = "up"
                    up = True
                    left = right = down = False

                elif e.key == K_DOWN:
                    hero.shutdirection = "down"
                    down = True
                    left = right = up = False

                if e.key == K_SPACE and not hero.isBullet:
                    bullet = Bullet(hero.rect.left,hero.rect.top,hero.shutdirection)
                    entities.add(bullet)
                    hero.isBullet = True

            if e.type == KEYUP:
                if e.key == K_RIGHT:
                    right = False
                elif e.key == K_LEFT:
                    left = False
                elif e.key == K_UP:
                    up = False
                elif e.key == K_DOWN:
                    down = False

        #выстрел монстра
        if mn.fire == 1 and not mn.isBullet:
            bullet_mn = Bullet(mn.rect.x,mn.rect.y,mn.shutdirection)
            entities.add(bullet_mn)
            mn.isBullet = True
            mn.fire = 0

        #движение пули героя
        if hero.isBullet:
            if mn.isBullet:
                bullet.update(platforms + [mn] + [bullet_mn])
            else:
                bullet.update(platforms + [mn])
            if bullet.bum >= 20:
                entities.remove(bullet)
                bullet = None
                hero.isBullet = False

        #движение пули монстра
        if mn.isBullet :
            if hero.isBullet:
                bullet_mn.update(platforms + [hero] + [bullet])
            else:
                bullet_mn.update(platforms + [hero])
            if bullet_mn.bum >= 20:
                entities.remove(bullet_mn)
                bullet_mn = None
                mn.isBullet = False

        #удаляем уничтоженные платформы
        for p in platforms:
            if (p.rect.width == 0) or (p.rect.height == 0):
                platforms.remove(p)

        hero.update(left, right, up, down, platforms + [mn]) # передвижение

        mn.update(platforms + [hero], hero.rect.top, hero.rect.left ) # передвигаем всех монстров

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать

        entities.draw(screen) # отображение всего

        pygame.display.update()     # обновление и вывод всех изменений на экран

if __name__ == "__main__":
    main()
