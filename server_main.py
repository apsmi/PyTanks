#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'apsmi'

import asyncore
import time
import pygame
import random
from server_dispatcher import Game_Server
from server_level import gen_level
from server_tank import Tank, Tank_config
from server_socket_loop import Socket_Loop

# основная функция сервера
def server_main():

    # серверный сокет
    game_server = Game_Server("", 80)

    #запускаем цикл опроса сокетов
    socket_loop_thread = Socket_Loop(asyncore.loop, 0.01)
    socket_loop_thread.start()

    # инициализация pygame
    pygame.init()

    # ждем двух клиентов
    while game_server.player_count != 2:
        time.sleep(1)

    # создаем уровень
    blocks = gen_level(30,30)

    # группы объектов
    players_yellow = pygame.sprite.Group()
    players_yellow_bullets = pygame.sprite.Group()
    players_green = pygame.sprite.Group()
    players_green_bullets = pygame.sprite.Group()

    # создаем героев
    player_config = Tank_config(34, 34)
    player1 = Tank(player_config)
    players_yellow.add(player1)

    player_config = Tank_config(768, 580)
    player2 = Tank(player_config)
    players_green.add(player2)

    for player in game_server.players:
        x = random.randint(32, 738)
        y = random.randint(32, 576)
        player_config = Tank_config(x, y)
        player_sprite = Tank(player_config)
        player.sprite = player_sprite
        if player.team == "green":
            players_green.add(player_sprite)
        else:
            players_yellow.add(player_sprite)

    # таймер
    timer = pygame.time.Clock()

    # Основной цикл программы
    while 1:

        timer.tick(30) # таймер на 30 кадров

        # TODO: read data from clients

        # обновление всех объектов
        players_yellow.update( blocks.sprites() + players_green.sprites() + players_yellow.sprites() )
        players_green.update( blocks.sprites() + players_yellow.sprites() + players_green.sprites() )
        players_yellow_bullets.update( blocks.sprites() + players_green.sprites() + players_green_bullets.sprites() )
        players_green_bullets.update( blocks.sprites() + players_yellow.sprites() + players_yellow_bullets.sprites() )

        # TODO: send data to clients

server_main()