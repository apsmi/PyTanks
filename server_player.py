# -*- coding: utf-8 -*-

# player states
IDLE = 0
WAIT_PLAYERS_COUNT = 1
WAIT_ALL_PLAYERS = 2

LEN_TERM = 4

import asynchat
import struct
import pickle

# серверный экземпляр клиента
class Game_Client(asynchat.async_chat):

    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)

        self.ac_in_buffer_size = 16384
        self.ac_out_buffer_size = 16384

        self.addr = addr
        self.ibuffer = []
        self.obuffer = b""
        self.imes = b""
        self.set_terminator(LEN_TERM)
        self.state = "len"
        self.team = ""
        self.sprite = 0
        self.last = {}

    def writable(self):
        return len(self.obuffer) > 0

    def handle_write(self):
        sent = self.sendto(self.obuffer, self.addr)
        self.obuffer = self.obuffer[sent:]

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):
        dataframe = b"".join(self.ibuffer)
        self.ibuffer = []
        if self.state == "len":
            self.state = "data"
            length = struct.unpack('L',dataframe)[0]
            self.set_terminator(length)
        elif self.state == "data":
            self.state = "len"
            self.set_terminator(LEN_TERM)
            self.imes = pickle.loads(dataframe)