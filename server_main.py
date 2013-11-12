#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'apsmirnov2'

import asyncore
import threading
import time
import pygame
from game_server import Game_Server
from server_level import gen_level
from server_tank import Tank, Tank_config

# отдельный поток для asyncore.loop
class Socket_Loop(threading.Thread):

    def __init__(self, function, arg):
        threading.Thread.__init__(self)
        self.function = function
        self.arg = arg

    def run(self):
        self.function(self.arg)

# основная функция сервера
def server_main():

    # серверный сокет
    game_server = Game_Server("", 80)

    #запускаем цикл опроса сокетов
    socket_loop_thread = Socket_Loop(asyncore.loop, 1)
    socket_loop_thread.start()

    # инициализация pygame
    pygame.init()

    # ждем двух клиентов
    while game_server.player_count != 2:
        time.sleep(1)

    # создаем уровень
    blocks = gen_level(30,30)

    # группы объектов
    players = pygame.sprite.Group()
    players_bullets = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    monsters_bullets = pygame.sprite.Group()

    # создаем героев
    player_config = Tank_config(34, 34)
    player1 = Tank(player_config)
    players.add(player1)

    player_config = Tank_config(768, 580)
    player2 = Tank(player_config)
    monsters.add(player2)

    # таймер
    timer = pygame.time.Clock()

    # Основной цикл программы
    while 1:

        timer.tick(60) # таймер на 60 кадров

server_main()