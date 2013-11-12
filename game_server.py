# -*- coding: utf-8 -*-

import asyncore
import socket
from game_client import Game_Client

# сокет, принимающий соединение от клиентов
class Game_Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen()
        self.player_count = 0
        self.player1 = None
        self.player2 = None

    def handle_accepted(self, sock, addr):
        if self.player_count == 0:
            self.player_count += 1
            self.player1 = Game_Client(sock, addr)
        elif self.player_count == 1:
            self.player_count += 1
            self.player2 = Game_Client(sock, addr)
        else:
            sock.close()