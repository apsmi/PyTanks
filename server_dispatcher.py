# -*- coding: utf-8 -*-

import asyncore
import socket
import struct
from server_player import Game_Client

# сокет, принимающий соединение от клиентов
class Game_Server_UDP(asyncore.dispatcher):

    # инициализация
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.player_count = 0 # количество подключенных клиентов
        self.players = []     # список пдключенных клиентов

    # входящее соедение - создается новый клиент
    def handle_read(self):

        # получем номер клиентского порта
        data, addr = self.recvfrom(4)
        client_port = struct.unpack('L',data)[0]
        print("Connected %s:%d, client port %d" % (addr[0], addr[1], client_port))

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
        self.players.append(player)
        if (self.player_count % 2) == 0 :
            player.team = "green"
        else:
            player.team = "yellow"