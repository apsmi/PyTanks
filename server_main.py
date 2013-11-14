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
from server_bullet import Bullet

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
    while game_server.player_count < 2:
        time.sleep(1)

    # создаем уровень
    blocks = gen_level(30,30)

    # группы объектов
    players_yellow = pygame.sprite.Group()
    players_yellow_bullets = pygame.sprite.Group()
    players_green = pygame.sprite.Group()
    players_green_bullets = pygame.sprite.Group()

    # создаем героев

    for player in game_server.players:
        x = random.randint(32, 738)
        y = random.randint(32, 576)
        player_config = Tank_config(x, y)
        player_sprite = Tank(player_config)
        player.sprite = player_sprite
        if player.team == "green":
            players_green.add(player_sprite)
        elif player.team == "yellow":
            players_yellow.add(player_sprite)

    # таймер
    timer = pygame.time.Clock()

    # Основной цикл программы
    while 1:

        timer.tick(30) # таймер на 30 кадров

        for player in game_server.players:
            event_queue = player.imes
            for e in event_queue:
                # действия  героя
                # нажатие клавиши на клавиатуре
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        player.sprite.course = "left"
                    elif e.key == pygame.K_RIGHT:
                        player.sprite.course = "right"
                    elif e.key == pygame.K_UP:
                        player.sprite.course = "up"
                    elif e.key == pygame.K_DOWN:
                        player.sprite.course = "down"
                    if e.key == pygame.K_SPACE and not player.sprite.isBullet:
                        player_bullet = Bullet(player.sprite.rect.left,player.sprite.rect.top,player.sprite.shutdirection)
                        player_bullet.shooter = player.sprite
                        if player.team == "green":
                            players_green_bullets.add(player_bullet)
                        elif player.team == "yellow":
                            players_yellow_bullets.add(player_bullet)
                        player.sprite.isBullet = True

                # отпускание клавиши
                if e.type == pygame.KEYUP:
                    if (e.key == pygame.K_RIGHT) and (player.course == "right"):
                        player.sprite.course = ""
                    elif (e.key == pygame.K_LEFT) and (player.course == "left"):
                        player.sprite.course = ""
                    elif (e.key == pygame.K_UP) and (player.course == "up"):
                        player.sprite.course = ""
                    elif (e.key == pygame.K_DOWN) and (player.course == "down"):
                        player.sprite.course = ""

        # обновление всех объектов
        players_yellow.update( blocks.sprites() + players_green.sprites() + players_yellow.sprites() )
        players_green.update( blocks.sprites() + players_yellow.sprites() + players_green.sprites() )
        players_yellow_bullets.update( blocks.sprites() + players_green.sprites() + players_green_bullets.sprites() )
        players_green_bullets.update( blocks.sprites() + players_yellow.sprites() + players_yellow_bullets.sprites() )

        # TODO: send data to clients

server_main()