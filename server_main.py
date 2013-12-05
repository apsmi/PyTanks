# -*- coding: utf-8 -*-

__author__ = 'apsmi'

#PLAYERS_COUNT = 1

#SERVER_ADDRESS = ''
#SERVER_PORT = 80

#LEVEL_H = 40
#LEVEL_W = 40

BLOCK_SIZE = 32
BLOCK_DEMAGE = 8

FRAME_RATE = 30

import asyncore
import argparse
import time
import pygame
import pygame._view
import random
import pickle
import struct
from server_dispatcher import Game_Server_UDP
from server_level import gen_level
from server_tank import Tank, Tank_config
from MyThread import MyThread
from server_bullet import Bullet

# подготовка пакета к передаче
def pack_data(data):
    tmp = pickle.dumps(data)
    l = len(tmp)
    return struct.pack('L', l) + tmp

# основная функция сервера
def server_main(PLAYERS_COUNT, SERVER_ADDRESS, SERVER_PORT, LEVEL_H, LEVEL_W):

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

    # серверный сокет
    game_server = Game_Server_UDP(SERVER_ADDRESS, SERVER_PORT, BLOCK_SIZE, LEVEL_W, LEVEL_H, players_green, players_yellow,
                    total_level_width, total_level_height, level_width, level_height, BLOCK_DEMAGE, FRAME_RATE, blocks)
    print("Server started on %s:%d" % (SERVER_ADDRESS, SERVER_PORT))
    print("Waiting for %d players..." % PLAYERS_COUNT)

    #запускаем цикл опроса сокетов
    socket_loop_thread = MyThread(asyncore.loop, [0.01] )
    socket_loop_thread.start()

    # таймер
    timer = pygame.time.Clock()

    # id пули
    bullet_id = 0

    # ждем первого клиента
    while game_server.player_count == 0:
        time.sleep(1)

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
            current = {'id': player.id, 'x': player.sprite.rect.x, 'y': player.sprite.rect.y,
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

        # упаковываем данные
        message = pack_data(dataframe)

        # отправляем
        for player in game_server.players:
            player.obuffer += message


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="port of the game server, default=80", type=int, default=80)
parser.add_argument("-c", "--count", help="count of players waiting to connect, default=2", type=int, default=2)
parser.add_argument("-v", "--vertical", help="vertical size (height) of world in blocks, default=30", type=int, default=30)
parser.add_argument("-w", "--width", help="width of world in blocks, default=30", type=int, default=30)
args = parser.parse_args()

#server_main(PLAYERS_COUNT, SERVER_ADDRESS, SERVER_PORT, LEVEL_H, LEVEL_W)
#server_main(1, "", 80, 30, 30)
server_main(args.count, "", args.port, args.vertical, args.width)
