# -*- coding: utf-8 -*-

import asyncore
import socket
import struct
import pickle
import random
import time
from server_tank import Tank, Tank_config
from server_player import Game_Client

# сокет, принимающий соединение от клиентов
class Game_Server_UDP(asyncore.dispatcher):

    # инициализация
    def __init__(self, host, port, BLOCK_SIZE, LEVEL_W, LEVEL_H, players_green, players_yellow,
                 total_level_width, total_level_height, level_width, level_height, BLOCK_DEMAGE, FRAME_RATE, blocks):
        asyncore.dispatcher.__init__(self)
        self.BLOCK_SIZE, self.LEVEL_W, self.LEVEL_H, self.players_green, self.players_yellow = \
            BLOCK_SIZE, LEVEL_W, LEVEL_H, players_green, players_yellow

        self.total_level_width, self.total_level_height, self.level_width, self.level_height, self.BLOCK_DEMAGE, self.FRAME_RATE, self.blocks = \
            total_level_width, total_level_height, level_width, level_height, BLOCK_DEMAGE, FRAME_RATE, blocks
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.player_count = 0 # количество подключенных клиентов
        self.players = []     # список пдключенных клиентов

    # подготовка пакета к передаче
    def pack_data(self, data):
        tmp = pickle.dumps(data)
        l = len(tmp)
        return struct.pack('L', l) + tmp

    # входящее соедение - создается новый клиент
    def handle_read(self):

        # получем номер клиентского порта
        data, addr = self.recvfrom(4)
        client_port = struct.unpack('L',data)[0]

        # создаем UPD сокет для клиента
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.bind(('', 0))
        server_port = socket_udp.getsockname()[1]

        # отправляем порт созданного сокета клиенту
        buf = struct.pack('L', server_port)
        socket_udp.sendto(buf, addr)

        # создаем нового клиента
        addr = (addr[0], client_port)
        self.player_count += 1
        player = Game_Client(socket_udp, addr)

        # создаем спрайт нового клиента
        x = random.randint(self.BLOCK_SIZE, (self.LEVEL_W - 2) * self.BLOCK_SIZE)
        y = random.randint(self.BLOCK_SIZE, (self.LEVEL_H - 2) * self.BLOCK_SIZE)
        player_config = Tank_config(x=x, y=y, speed=2, lifes=1, dead_count=15)
        player_sprite = Tank(player_config)
        player.sprite = player_sprite

        # идентификатор создаваемого игрока
        player.id = server_port

        # определяем команду нового клиента
        if (self.player_count % 2) == 0 :
            player.team = "green"
            self.players_green.add(player_sprite)
        else:
            player.team = "yellow"
            self.players_yellow.add(player_sprite)
        self.players.append(player)

        # отправить текущую конфигурацию уровня
        dataframe = {}

        # формируем список параметров
        dataframe['params'] = {'total_width': self.total_level_width, 'total_height': self.total_level_height, 'width': self.level_width,
                              'height': self.level_height, 'block_demage': self.BLOCK_DEMAGE, 'frame_rate': self.FRAME_RATE}

        #блоки
        dataframe['blocks'] = []
        for b in self.blocks.sprites():
            data = {'id' : b.id, 'x' : b.rect.x, 'y' : b.rect.y, 'type' : b.type, 'hits': b.hits}
            dataframe['blocks'].append(data)

        #игроки
        dataframe['players'] = []
        for gamer in self.players:
            data = {'id' : gamer.id, 'x' : gamer.sprite.rect.x, 'y' : gamer.sprite.rect.y, 'team' : gamer.team, 'dead_count': gamer.sprite.config.dead_count}
            dataframe['players'].append(data)

        # упаковываем данные
        message = self.pack_data(dataframe)

        # отправляем
        player.obuffer += message
        player.ready = True

        print("Connected client %s:%d, team: %s" % (addr[0], addr[1], player.team))