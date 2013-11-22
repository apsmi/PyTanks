# -*- coding: utf-8 -*-

# player states

IN_BUF_SIZE = 16384   # размер  входящего буфера сокета
OUT_BUF_SIZE = 16384  # размер исходящего буфера сокета
LEN_TERM = 4          # размера первой части сообщения, содержащего длину - одно целое число 4 байта

import asynchat
import struct
import pickle

# серверный экземпляр клиента
class Game_Client(asynchat.async_chat):

    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.ac_in_buffer_size = IN_BUF_SIZE
        self.ac_out_buffer_size = OUT_BUF_SIZE
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