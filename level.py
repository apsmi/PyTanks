# -*- coding: utf-8 -*-

"""
Генератор уровней.

Объекты:
"*" - не уничтожаемый, границы уровня;
"-" - уничтожаемый объект.

"""

import random

from blocks import BlockWidget, PLATFORM_HEIGHT, PLATFORM_WIDTH


def gen_level(height, width):

    level = []  # матрица, содержащая уровень

    for y in range(height):

        line = ""  # строка матрицы уровня
        for x in range(width):

            item = " "  # блок
            if 8 < random.randint(0, 10):
                item = "-"
            if y == 0 or y == (height-1) or x == 0 or x == (width - 1):
                item = "*"

            line += item

        level.append(line)

    total_level_width = len(level[0])*PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня в пикселах
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту

    blocks = []

    #рисуем платформы
    x = y = 0  # координаты
    for row in level:          # вся строка
        for col in row:        # каждый символ
            if col == "-" or col == "*":
                pf = BlockWidget(x, y, col)
                blocks.append(pf)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    # то же самое и с высотой
        x = 0                   # на каждой новой строчке начинаем с нуля

    return blocks, total_level_width, total_level_height