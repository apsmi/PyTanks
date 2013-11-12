# -*- coding: utf-8 -*-

# player states
IDLE = 0
WAIT_PLAYERS_COUNT = 1
WAIT_ALL_PLAYERS = 2

import asynchat

# серверный экземпляр клиента
class Game_Client(asynchat.async_chat):

    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.ibuffer = []
        self.obuffer = b""
        self.dataframe = []
        self.set_terminator(b"\x00")
        self.state = WAIT_ALL_PLAYERS

    def writable(self):
        return len(self.obuffer) > 0

    def handle_write(self):
        sent = self.send(self.obuffer)
        self.obuffer = self.obuffer[sent:]

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):

        self.dataframe = self.ibuffer
        self.ibuffer = []