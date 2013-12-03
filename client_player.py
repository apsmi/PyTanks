# -*- coding: utf-8 -*-
__author__ = 'apsmi'

import asynchat, socket, struct, pickle

IN_BUF_SIZE = 16384   # размер  входящего буфера сокета
OUT_BUF_SIZE = 16384  # размер исходящего буфера сокета

LEN_TERM = 4

# сокет, принимающий соединение от клиентов
class Client(asynchat.async_chat):

    def __init__(self, addr):
        asynchat.async_chat.__init__(self)
        self.ibuffer = []
        self.obuffer = b""
        self.imes = [] #b""

        # создаем сокет
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('', 0))
        client_port = self.socket.getsockname()[1]

        # подключаемся к диспетчеру, отправляем ему свой клиентский порт
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))
        sock.sendto(struct.pack('L', client_port), addr)

        # получем серверный udp порт
        buf, _ = sock.recvfrom(4)
        server_port = struct.unpack('L',buf)[0]
        sock.close()

        self.ac_in_buffer_size = IN_BUF_SIZE
        self.ac_out_buffer_size = OUT_BUF_SIZE

        self.addr = (addr[0], server_port)
        self.set_terminator(LEN_TERM)
        self.state = "len"

    def handle_close(self):
        #print(self.socket.getsockname())
        self.close()

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
            self.imes.append(pickle.loads(dataframe))
            if self.imes == "exit":
                self.close()