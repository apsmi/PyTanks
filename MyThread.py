# -*- coding: utf-8 -*-
__author__ = 'apsmi'

import threading

class MyThread(threading.Thread):

    def __init__(self, function, *arg):
        threading.Thread.__init__(self)
        self.function = function
        self.arg = arg

    def run(self):
        self.function(self.arg)