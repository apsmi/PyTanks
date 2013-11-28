#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame._view
import pygame
import pyganim
import eztext
import MyThread
import server_main

def window_init(width, height, color, caption):
    display = (width, height)                   # Группируем ширину и высоту в одну переменную
    screen = pygame.display.set_mode(display)   # Создаем окошко
    pygame.display.set_caption(caption)         # Пишем в шапку
    bg = pygame.Surface((width,height))                # Создание видимой поверхности, будем использовать как фон
    bg.fill(pygame.Color(color))                       # Заливаем поверхность сплошным цветом
    return bg, screen

def title_screen(background, screen, WINDOW_W, WINDOW_H):

    # шрифт
    font = pygame.font.Font('freesansbold.ttf', 14)

    # надписи
    label_hint = font.render("Tab - навигация, Enter - выбор, Esc - выход", True, (255, 255, 166), (0,0,0))
    hint_x = WINDOW_W/2 - label_hint.get_width()/2
    hint_y = 10

    font = pygame.font.Font('freesansbold.ttf', 18)
    label_create = font.render("Создать новую игру", True, (255, 255, 166), (0,0,0))
    label_join = font.render("Присоединиться к игре", True, (255, 255, 166), (0,0,0))

    # координаты
    label_coords = {'create': (hint_x+40, 100), 'join': (hint_x+40, 150)}
    cursor_coords = {'create': (hint_x, 95), 'join': (hint_x, 145)}

    cursor = pygame.image.load('tanks\player1_1.png')

    ANIMATION = ['tanks\player1_1.png', 'tanks\player1_2.png']
    boltAnim = []
    for anim in ANIMATION:
        boltAnim.append((anim, 0.1))
    boltAnimMove = pyganim.PygAnimation(boltAnim)
    boltAnimMove.play()

    timer = pygame.time.Clock()

    selected = 'create'

    while True:
        timer.tick(30) # fps
        screen.blit(background, (0,0)) # clear screen

        for e in pygame.event.get():
            # выход
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return "quit", hint_x

            # нажатие клавиши на клавиатуре
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return selected, hint_x
                elif e.key == pygame.K_TAB:
                    if selected == 'create':
                        selected = 'join'
                    else:
                        selected = 'create'

        # вывод надписей
        screen.blit(label_hint, (hint_x,hint_y))
        screen.blit(label_create, label_coords['create'])
        screen.blit(label_join, label_coords['join'])
        # и курсора
        cursor.fill(pygame.Color("#000000"))
        cursor.set_colorkey(pygame.Color("#000000"))
        boltAnimMove.blit(cursor, (0, 0))
        cursor = pygame.transform.rotate(cursor, 270)
        screen.blit(cursor, cursor_coords[selected])

        # обновление и вывод всех изменений на экран
        pygame.display.update()

    return selected, hint_x

def create_game(background, screen, hint_x, WINDOW_W, WINDOW_H):

    # шрифт
    font = pygame.font.Font('freesansbold.ttf', 14)

    # надписи
    label_hint = font.render("Tab - навигация, Backspace - стереть, Enter - продолжить, Esc - выход", True, (255, 255, 166), (0,0,0))
    hint_x_new = WINDOW_W/2 - label_hint.get_width()/2
    hint_y = 10

    font = pygame.font.Font('freesansbold.ttf', 18)
    players_count = eztext.Input(x=hint_x+40, y=100, maxlength=25, color=(255,255,166),  prompt='Количество танков: ', font=font)
    name_box = eztext.Input(x=hint_x+40, y=150, maxlength=25, color=(255,255,166),       prompt='Название танка:    ', font=font)
    label_error = font.render("Количество игроков должно быть целым числом!!!", True, (255, 0, 0), (0,0,0))
    err_x = WINDOW_W/2 - label_error.get_width()/2

    # координаты
    cursor_coords = {'count': (hint_x, 95), 'name': (hint_x, 145)}

    cursor = pygame.image.load('tanks\player1_1.png')

    ANIMATION = ['tanks\player1_1.png', 'tanks\player1_2.png']
    boltAnim = []
    for anim in ANIMATION:
        boltAnim.append((anim, 0.1))
    boltAnimMove = pyganim.PygAnimation(boltAnim)
    boltAnimMove.play()

    timer = pygame.time.Clock()
    error = False
    selected = 'count'

    while True:
        timer.tick(30) # fps
        screen.blit(background, (0,0)) # clear screen

        events = pygame.event.get()
        for e in events:
            # выход
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return "quit", "quit"

            # нажатие клавиши на клавиатуре
            if e.type == pygame.KEYDOWN:
                error = False
                if e.key == pygame.K_RETURN:
                    if not players_count.value.isdigit():
                        error = True
                    else:
                        return players_count.value, name_box.value
                elif e.key == pygame.K_TAB:
                    if selected == 'count':
                        selected = 'name'
                    else:
                        selected = 'count'

        # обновляем текст
        if selected == 'count':
            players_count.update(events)
        elif selected == 'name':
            name_box.update(events)

        # вывод надписей
        screen.blit(label_hint, (hint_x_new,hint_y))
        players_count.draw(screen)
        name_box.draw(screen)

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

    return players_count.value, name_box.value

def main():

    WINDOW_W = 800
    WINDOW_H = 640

    # Инициация PyGame, обязательная строчка
    pygame.init()

    #  инициализация окна
    background, screen = window_init(WINDOW_W, WINDOW_H, "#000000", "PyTanks")

    create_or_join = ""
    started = False

    while not started:

        create_or_join, hint_x = title_screen(background, screen, WINDOW_W, WINDOW_H)

        if create_or_join == 'create':
            create_or_join = ""
            players_count, player_name = create_game(background, screen, hint_x, WINDOW_W, WINDOW_H)

            #запускаем сервер
            #server_main(PLAYERS_COUNT, SERVER_ADDRESS, SERVER_PORT, LEVEL_H, LEVEL_W)
            server_thread = MyThread.MyThread(server_main.server_main, int(players_count), "", 80, 30, 30)
            server_thread.start()

        elif create_or_join == 'join':
            pass

        elif create_or_join == 'quit':
            started = True

    pygame.quit()
    return

if __name__ == "__main__":
    main()