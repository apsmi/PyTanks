__author__ = 'cam'

#генератор уровней
"""
Объекты
"-" -  не уничтожаемый, границы уровня
"*" - уничтожаемый объект
"""

import random

def gen_level():
    height = 30
    weidth = 30
    level = []
    for y in range(weidth):
        st_line = ""

        for x in range(height):
            line = " "
            if 7 < random.randint (0, 10) :
                line = "*"
            if y == 0 or y == (height-1) or x == 0 or x == (weidth - 1):
                line = "-"
            st_line = st_line + line
        level.append(st_line)
    print (level)
    return level

gen_level()
