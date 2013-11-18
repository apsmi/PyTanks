# -*- coding: utf-8 -*-

#генератор уровней
"""
Объекты
"-" -  не уничтожаемый, границы уровня
"*" - уничтожаемый объект
"""

import random
import pygame
from blocks import Block, PLATFORM_HEIGHT, PLATFORM_WIDTH

def gen_level(height, width):

    level = []

    for y in range(height):

        st_line = ""
        for x in range(width):

            line = " "
            if 8 < random.randint (0, 10) :
                line = "-"
            if y == 0 or y == (height-1) or x == 0 or x == (width - 1):
                line = "*"

            st_line = st_line + line

        level.append(st_line)

    level[1] = level[1][:1] + " " + level[1][2:]
    level[height-2] = level[height-2][:width-2] + " " + level[height-2][width-1:]

    blocks = pygame.sprite.Group()

    #рисуем платформы
    id = 0
    x=y=0 # координаты
    for row in level:          # вся строка
        for col in row:        # каждый символ
            if col == "-" or col == "*":
                pf = Block(x,y,col, id)
                id += 1
                blocks.add(pf)
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля

    return blocks