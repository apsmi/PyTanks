# -*- coding: utf-8 -*-

#генератор уровней
"""
Объекты
"-" -  не уничтожаемый, границы уровня
"*" - уничтожаемый объект
"""

import pygame
from client_blocks import Block

def gen_client_level(blocks_list, block_demage):

    blocks = pygame.sprite.Group()

    #рисуем платформы
    #x=y=0 # координаты
    for block in blocks_list:          # вся строка

        # {'id' : b.id, 'x' : b.rect.x, 'y' : b.rect.y, 'type' : b.type, 'hits': b.hits}

        id = block["id"]
        x = block["x"]
        y = block["y"]
        type = block["type"]
        hits = block["hits"]

        b = Block(id, x, y, type, block_demage)
        blocks.add(b)

        for hit in hits:
            b.die(hit)

    return blocks