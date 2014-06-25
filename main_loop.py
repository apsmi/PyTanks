# -*- coding: utf-8 -*-

import sys
import pygame
from pygame import *

from level import gen_level
from bullet import Bullet
from tank import Tank_config, Tank
from monster_config import *
from camera import  camera_configure, Camera

from monster import Monster


def window_init(width, height, color, caption):
    display = (width, height)                   # Группируем ширину и высоту в одну переменную
    pygame.init()                               # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(display)   # Создаем окошко
    pygame.display.set_caption(caption)         # Пишем в шапку
    bg = Surface((width, height))                # Создание видимой поверхности, будем использовать как фон
    bg.fill(Color(color))                       # Заливаем поверхность сплошным цветом
    return bg, screen


def main_loop_prepare():
    # инициализация окна TODO: change to kivy
    #bg, screen = window_init(800, 480, "#000000", "PyTanks")

    # группы объектов
    players = pygame.sprite.Group()
    players_bullets = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    monsters_bullets = pygame.sprite.Group() # перемещено в глобальную переменную

    # создаем героя
    player_config = Tank_config()
    player = Tank(player_config)
    players.add(player)

    # монстр 1
    monster_config = Monster_config_1(704,580)
    monster = Monster(monster_config)
    monsters.add(monster)

    # монстр 1
    monster_config = Monster_config_2(736,580)
    monster = Monster(monster_config)
    monsters.add(monster)

    # монстр 1
    monster_config = Monster_config_3(768,580)
    monster = Monster(monster_config)
    monsters.add(monster)

    # генерируем уровень
    blocks, total_level_width, total_level_height = gen_level(30,30)

    #создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height)

    return player, players_bullets, players, blocks, monsters, monsters_bullets, camera


def main_loop(player, players_bullets, players, blocks, monsters, monsters_bullets, camera, screen, bg):

    # таймер
    #timer = pygame.time.Clock()

    # Основной цикл программы
    #while 1:
    if True:

        #timer.tick(60)  # таймер на 60 кадров

        # обновление всех объектов
        players.update(blocks.sprites() + monsters.sprites())
        players_bullets.update(blocks.sprites() + monsters.sprites() + monsters_bullets.sprites())
        monsters_bullets.update(blocks.sprites() + players.sprites() + players_bullets.sprites())
        monsters.update(blocks.sprites() + players.sprites() + monsters.sprites(), player.rect.top, player.rect.left,
                        monsters_bullets)
        camera.update(player)  # центризируем камеру относительно персонажа

        # Каждую итерацию необходимо всё перерисовывать TODO: change to kivy
        #screen.blit(bg, (0, 0))

        # рисование всех объектов
        entities = blocks.sprites() + players.sprites() + players_bullets.sprites() + monsters_bullets.sprites() + monsters.sprites()
        for e in entities:
            screen.blit(e.image, camera.apply(e))  # TODO: change to kivy

        # обновление и вывод всех изменений на экран TODO: change to kivy
        #pygame.display.update()