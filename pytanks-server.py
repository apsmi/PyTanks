#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'apsmirnov2'

import asyncore, socket, asynchat, time, threading

# сокет, принимающий соединение от клиентов
class Game_Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(2)
    def handle_accepted(self, sock, addr):
        print('\r\nIncoming connection from %s' % repr(addr))
        handler = Game_Client(sock, addr)

# серверный экземпляр клиента
class Game_Client(asynchat.async_chat):
    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.ibuffer = []
        self.obuffer = b""
        self.set_terminator(b"\x00")
        self.last_sent_time = time.time()
    def writable(self):
        now = time.time()
        diff = abs(now - self.last_sent_time)
        if diff > 1:
            self.last_sent_time = now
            if len(self.obuffer) <= 0:
                self.obuffer = b"server send\x00"
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

class Socket_Loop(threading.Thread):
    def __init__(self, function, arg):
        threading.Thread.__init__(self)
        self.function = function
        self.arg = arg
    def run(self):
        self.function(self.arg)

game_server = Game_Server("", 80)

#запускаем цикл опроса сокетов
socket_loop_thread = Socket_Loop(asyncore.loop, 1)
socket_loop_thread.start()
print("Thread started")
socket_loop_thread.join()