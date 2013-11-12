#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'apsmirnov2'

import asyncore, socket, asynchat, time

# сокет, принимающий соединение от клиентов
class Client(asynchat.async_chat):
    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        self.obuffer = b""
        self.ibuffer = []
        self.set_terminator(b"\x00")
        self.last_sent_time = time.time()
    def writable(self):
        now = time.time()
        diff = abs(now - self.last_sent_time)
        if diff > 5:
            self.last_sent_time = now
            if len(self.obuffer) <= 0:
                self.obuffer = b"client send\x00"
            return (len(self.obuffer) > 0)
    def handle_write(self):
        sent = self.send(self.obuffer)
        self.obuffer = self.obuffer[sent:]
    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer.append(data)
    def found_terminator(self):
        self.dataframe = self.ibuffer
        self.ibuffer = []
        print("From " + str(self.addr) + " receive: " + str(self.dataframe) )



client = Client("localhost", 80)

#запускаем цикл опроса сокетов
asyncore.loop(1)