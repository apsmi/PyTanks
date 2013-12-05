#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame._view
import pygame
import pyganim
import eztext
#import MyThread
#import server_main
import client_main

def window_init(width, height, color, caption):
    display = (width, height)                   # Группируем ширину и высоту в одну переменную
    screen = pygame.display.set_mode(display)   # Создаем окошко
    pygame.display.set_caption(caption)         # Пишем в шапку
    bg = pygame.Surface((width,height))                # Создание видимой поверхности, будем использовать как фон
    bg.fill(pygame.Color(color))                       # Заливаем поверхность сплошным цветом
    return bg, screen

def title_screen(background, screen, WINDOW_W, WINDOW_H):

    # шрифт
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 14)

    # надпись с подсказкой
    label_hint = font.render("Стрелки вверх/вниз - навигация, Enter - выбор, Esc - выход", True, (255, 255, 166), (0,0,0))
    hint_x = WINDOW_W/2 - label_hint.get_width()/2
    hint_y = 10

    # новый шрифт
    font = pygame.font.Font('freesansbold.ttf', 18)

    # координаты
    cursor_coords = {'server': (hint_x, 95), 'port': (hint_x, 145), 'name': (hint_x, 195)}

    # inputbox'ы
    box_server = eztext.Input(x=hint_x+40, y=100, maxlength=25, color=(255,255,166), prompt='Адрес сервера: ', font=font)
    box_port = eztext.Input(x=hint_x+40, y=150, maxlength=25, color=(255,255,166),   prompt='Порт сервера:  ', font=font)
    box_name = eztext.Input(x=hint_x+40, y=200, maxlength=25, color=(255,255,166),   prompt='Имя игрока:    ', font=font)

    # ошибка
    label_error = font.render("Порт сервера должен быть целым числом, а имя не должно быть пустым", True, (255, 0, 0), (0,0,0))
    err_x = WINDOW_W/2 - label_error.get_width()/2

    # танчик-курсор
    cursor = pygame.image.load('tanks\player1_1.png')

    # его анимация
    ANIMATION = ['tanks\player1_1.png', 'tanks\player1_2.png']
    boltAnim = []
    for anim in ANIMATION:
        boltAnim.append((anim, 0.1))
    boltAnimMove = pyganim.PygAnimation(boltAnim)
    boltAnimMove.play()

    timer = pygame.time.Clock()

    selected = 'server'
    error = False

    while True:
        timer.tick(30) # fps
        screen.blit(background, (0,0)) # clear screen

        events = pygame.event.get()
        for e in events:
            # выход
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return "quit", "quit", "quit"

            # нажатие клавиши на клавиатуре
            if e.type == pygame.KEYDOWN:
                error = False

                # если нажали Enter
                if e.key == pygame.K_RETURN:

                    # проверяем правильность ввода
                    if (not box_port.value.isdigit()) or (box_name.value == ""):
                        error = True
                    else:
                        return box_server.value, box_port.value, box_name.value

                # если стрелки, двигаем курсор
                elif (e.key == pygame.K_DOWN) or (e.key == pygame.K_TAB):
                    if selected == 'server':
                        selected = 'port'
                    elif selected == 'port':
                        selected = 'name'
                    else:
                        selected = 'server'
                elif e.key == pygame.K_UP:
                    if selected == 'server':
                        selected = 'name'
                    elif selected == 'port':
                        selected = 'server'
                    else:
                        selected = 'port'

        # обновляем текст
        if selected == 'server':
            box_server.update(events)
        elif selected == 'port':
            box_port.update(events)
        elif selected == 'name':
            box_name.update(events)

        # вывод надписей
        screen.blit(label_hint, (hint_x,hint_y))
        box_server.draw(screen)
        box_port.draw(screen)
        box_name.draw(screen)

        # и курсора
        cursor.fill(pygame.Color("#000000"))
        cursor.set_colorkey(pygame.Color("#000000"))
        boltAnimMove.blit(cursor, (0, 0))
        cursor = pygame.transform.rotate(cursor, 270)
        screen.blit(cursor, cursor_coords[selected])

        # и сообщения об ошибке
        if error:
            screen.blit(label_error, (err_x, 200))

        # обновление и вывод всех изменений на экран
        pygame.display.update()

    return box_server.value, box_port.value, box_name.value

def main():

    WINDOW_W = 800
    WINDOW_H = 640

    # Инициация PyGame, обязательная строчка
    pygame.init()

    #  инициализация окна
    background, screen = window_init(WINDOW_W, WINDOW_H, "#000000", "PyTanks")

    quit_flag = False

    while not quit_flag:

        # выводим титульное меню
        server, port, player_name = title_screen(background, screen, WINDOW_W, WINDOW_H)

        # выход из цикла
        if (server == 'quit') or (port == 'quit') or (player_name == 'quit'):
            quit_flag = True

        else:
            # client_main(background, screen, SERVER_ADDR, SERVER_PORT_DISP)
            client_main.client_main(background, screen, WINDOW_W, WINDOW_H, server, int(port), player_name)

    pygame.quit()
    return

if __name__ == "__main__":
    main()