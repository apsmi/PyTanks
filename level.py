# -*- coding: utf-8 -*-
__author__ = 'cam'

#генератор уровней
"""
Объекты
"-" -  не уничтожаемый, границы уровня
"*" - уничтожаемый объект
"""

import random

def gen_level(height,weidth):
    level = []
    for y in range(height):
        st_line = ""

        for x in range(weidth):
            line = " "
            if 8 < random.randint (0, 10) :
                line = "-"
            if y == 0 or y == (height-1) or x == 0 or x == (weidth - 1):
                line = "*"
            st_line = st_line + line
        level.append(st_line)
    level[1] = level[1][:1] + " " + level[1][2:]
    level[height-2] = level[height-2][:weidth-2] + " " + level[height-2][weidth-1:]
    return level

gen_level(20,25)
