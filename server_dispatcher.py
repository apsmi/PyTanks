# -*- coding: utf-8 -*-

import asyncore
import socket
from server_player import Game_Client

# сокет, принимающий соединение от клиентов
class Game_Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.player_count = 0
        self.players = []

    def handle_accepted(self, sock, addr):
        if self.player_count < 2:

            print("connected %s:%d" % (addr[0], addr[1]))

            self.player_count += 1
            player = Game_Client(sock, addr)
            self.players.append(player)
            if (self.player_count) % 2 == 0 :
                player.team = "green"
            else:
                player.team = "yellow"
        else:
            sock.close()
