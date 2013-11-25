#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'apsmi'

PLAYERS_COUNT = 1

SERVER_ADDRESS = ''
SERVER_PORT = 80

LEVEL_H = 40
LEVEL_W = 40

BLOCK_SIZE = 32
BLOCK_DEMAGE = 8

FRAME_RATE = 30

import asyncore
import time
import pygame
import random
import pickle
import struct
from server_dispatcher import Game_Server_UDP
from server_level import gen_level
from server_tank import Tank, Tank_config
from server_socket_loop import Socket_Loop
from server_bullet import Bullet

# подготовка пакета к передаче
def pack_data(data):
    tmp = pickle.dumps(data)
    l = len(tmp)
    return struct.pack('L', l) + tmp

# основная функция сервера
def server_main(PLAYERS_COUNT, SERVER_ADDRESS, SERVER_PORT, LEVEL_H, LEVEL_W, BLOCK_SIZE, BLOCK_DEMAGE, FRAME_RATE):

    # серверный сокет
    game_server = Game_Server_UDP(SERVER_ADDRESS, SERVER_PORT)
    print("Server started on %s:%d" % (SERVER_ADDRESS, SERVER_PORT))
    print("Waiting for %d players..." % PLAYERS_COUNT)

    #запускаем цикл опроса сокетов
    socket_loop_thread = Socket_Loop(asyncore.loop, 0.01)
    socket_loop_thread.start()

    # инициализация pygame
    pygame.init()

    # создаем уровень
    level_height = LEVEL_H
    level_width = LEVEL_W
    blocks, total_level_width, total_level_height = gen_level(level_height,level_width, BLOCK_DEMAGE)

    # группы объектов
    players_yellow = pygame.sprite.Group()
    players_yellow_bullets = pygame.sprite.Group()
    players_green = pygame.sprite.Group()
    players_green_bullets = pygame.sprite.Group()

    # ждем клиентов
    while game_server.player_count < PLAYERS_COUNT:
        time.sleep(1)

    # создаем героев
    for player in game_server.players:
        x = random.randint(BLOCK_SIZE, (LEVEL_W - 2) * BLOCK_SIZE)
        y = random.randint(BLOCK_SIZE, (LEVEL_H - 2) * BLOCK_SIZE)
        player_config = Tank_config(x=x, y=y, speed=2, lifes=1, dead_count=30)
        player_sprite = Tank(player_config)
        player.sprite = player_sprite
        if player.team == 'green':
            players_green.add(player_sprite)
        elif player.team == 'yellow':
            players_yellow.add(player_sprite)

    # отправить идентификаторы игрокам
    for player in game_server.players:
        message = pack_data(player.addr[0])
        player.obuffer += message

    # отправить начальную конфигурацию уровня
    dataframe = {}

    # передаем параметры
    dataframe['params'] = {'total_width': total_level_width, 'total_height': total_level_height, 'width': level_width,
                          'height': level_height, 'block_demage': BLOCK_DEMAGE}

    #блоки
    dataframe['blocks'] = []
    for b in blocks.sprites():
        data = {'id' : b.id, 'x' : b.rect.x, 'y' : b.rect.y, 'type' : b.type}
        dataframe['blocks'].append(data)

    #игроки
    dataframe['players'] = []
    for player in game_server.players:
        data = {'id' : player.addr[0], 'x' : player.sprite.rect.x, 'y' : player.sprite.rect.y, 'team' : player.team, 'dead_count': player.sprite.config.dead_count}
        dataframe['players'].append(data)

    # упаковываем данные
    message = pack_data(dataframe)

    # отправляем
    for player in game_server.players:
        player.obuffer += message

    # таймер
    timer = pygame.time.Clock()

    # id пули
    bullet_id = 0

    # Основной цикл программы
    while 1:

        timer.tick(FRAME_RATE)                    # таймер на 30 кадров
        print('\rserver FPS: %.2f   ' % timer.get_fps(), end='') # вывод fps

        # цикл по всем игрокам
        for player in game_server.players:

            if player.socket._closed:
                print('\nDisconnected client %s:%d, team: %s' % (player.addr[0], player.addr[1], player.team))
                game_server.players.remove(player)
                game_server.player_count -= 1
                if game_server.player_count <= 0:
                    pygame.quit()
                    game_server.close()
                    print("All players disconnected")
                    return

            # очередь событий текущего игрока
            event_queue = player.imes

            # цикл по всем событиям в очереди
            for e in event_queue:

                type = e['type'] # тип события
                key = e['key']   # нажатая клавиша

                # нажатие клавиши на клавиатуре
                if type == pygame.KEYDOWN:

                    # движение
                    if key == pygame.K_LEFT:
                        player.sprite.course = 'left'
                    elif key == pygame.K_RIGHT:
                        player.sprite.course = 'right'
                    elif key == pygame.K_UP:
                        player.sprite.course = 'up'
                    elif key == pygame.K_DOWN:
                        player.sprite.course = 'down'

                    # выстрел
                    if key == pygame.K_SPACE and not player.sprite.isBullet:
                        player_bullet = Bullet(bullet_id,player.sprite.rect.left,player.sprite.rect.top,player.sprite.shutdirection)
                        bullet_id += 1
                        player_bullet.shooter = player.sprite
                        if player.team == 'green':
                            players_green_bullets.add(player_bullet)
                        elif player.team == 'yellow':
                            players_yellow_bullets.add(player_bullet)
                        player.sprite.isBullet = True

                # отпускание клавиши
                if type == pygame.KEYUP:
                    if (key == pygame.K_RIGHT) and (player.sprite.course == 'right'):
                        player.sprite.course = ''
                    elif (key == pygame.K_LEFT) and (player.sprite.course == 'left'):
                        player.sprite.course = ''
                    elif (key == pygame.K_UP) and (player.sprite.course == 'up'):
                        player.sprite.course = ''
                    elif (key == pygame.K_DOWN) and (player.sprite.course == 'down'):
                        player.sprite.course = ''

        # обновление всех объектов (симуляция мира)
        players_yellow.update( blocks.sprites() + players_green.sprites() + players_yellow.sprites() )
        players_green.update( blocks.sprites() + players_yellow.sprites() + players_green.sprites() )
        players_yellow_bullets.update( blocks.sprites() + players_green.sprites() + players_green_bullets.sprites() )
        players_green_bullets.update( blocks.sprites() + players_yellow.sprites() + players_yellow_bullets.sprites() )

        # отправить очередные изменения мира
        dataframe = {}

        #блоки
        dataframe['blocks'] = []
        for b in blocks.sprites():
            if b.shooted:
                data = {'id' : b.id, 'shootdirection' : b.shootdirection}
                dataframe['blocks'].append(data)
                b.shooted = False
                b.shootdirection = ''
            if b.dead:
                b.kill()

        #игроки
        dataframe['players'] = []
        for player in game_server.players:
            current = {'id': player.addr[0], 'x': player.sprite.rect.x, 'y': player.sprite.rect.y,
                        'course': player.sprite.course, 'shutdirection': player.sprite.shutdirection,
                        'dead': player.sprite.dead}
            if player.last != current :
                dataframe['players'].append(current)
            player.last = current

        #пули
        dataframe['bullets'] = []
        for b in players_yellow_bullets.sprites() + players_green_bullets.sprites():
            data = {'id': b.id, 'x': b.rect.x, 'y': b.rect.y, 'shutdirection' : b.shutdirection, 'bum': b.bum}
            dataframe['bullets'].append(data)
            if b.dead:
                b.kill()

        # упаковываем данные
        message = pack_data(dataframe)

        # отправляем
        for player in game_server.players:
            player.obuffer += message

server_main(PLAYERS_COUNT, SERVER_ADDRESS, SERVER_PORT, LEVEL_H, LEVEL_W, BLOCK_SIZE, BLOCK_DEMAGE, FRAME_RATE)
