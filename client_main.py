# -*- coding: utf-8 -*-

import pygame
import pygame._view
import time
import asyncore
import pickle
import struct
from pygame import Surface, Color

from client_player import Client
from client_level import gen_client_level
from client_bullet import Bullet
from MyThread import MyThread
from client_camera import  camera_configure, Camera
from client_tank import Tank, Tank_config

#SERVER_ADDR = '10.12.129.70'
#SERVER_ADDR = 'localhost'
#SERVER_PORT_DISP = 80
#WINDOW_W = 800
#WINDOW_H = 640

MAX_LEN_QUEUE = 3

def window_init(width, height, color, caption):
    display = (width, height)                   # Группируем ширину и высоту в одну переменную
    screen = pygame.display.set_mode(display)   # Создаем окошко
    pygame.display.set_caption(caption)         # Пишем в шапку
    bg = Surface((width,height))                # Создание видимой поверхности, будем использовать как фон
    bg.fill(Color(color))                       # Заливаем поверхность сплошным цветом
    return bg, screen

def pack_data(data):
    tmp = pickle.dumps(data)
    l = len(tmp)
    return struct.pack('L', l) + tmp

def client_main(bg, screen, WINDOW_W, WINDOW_H, SERVER_ADDR, SERVER_PORT_DISP, player_name):

    # Инициация PyGame, обязательная строчка
    #pygame.init()
    #pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

    #  инициализация окна
    #bg, screen = window_init(WINDOW_W, WINDOW_H, "#000000", "PyTanks")

    # группы объектов
    players = pygame.sprite.Group()
    players_bullets = pygame.sprite.Group()

    # создаем асинхронный клиент
    game_client = Client((SERVER_ADDR, SERVER_PORT_DISP))

    # запускаем цикл опроса сокетов
    socket_loop_thread = MyThread(asyncore.loop, [0.01])
    socket_loop_thread.start()

    # отправляем серверу свое имя
    message = pack_data(player_name)
    #game_client.obuffer = message

    # получаем собственный идентификатор
    #while len(game_client.imes) <= 0:
        #time.sleep(1)
    my_id = player_name

    # получаем первоначальную инфу
    flag = True
    while flag:
        if len(game_client.imes) > 0:
            data = game_client.imes.pop(0)
            if 'params' in data.keys():
                init_data = data
                flag = False

    #print(game_client.imes)
    #init_data = game_client.imes.pop(0)

    FRAME_RATE = init_data['params']['frame_rate']
    #['params'] = {'total_width': total_level_width, 'total_height': total_level_height, 'width': level_width,
    #                      'height': level_height, 'block_demage': BLOCK_DEMAGE}

    # генерируем уровень
    total_level_width = init_data['params']['total_width']
    total_level_height = init_data['params']['total_height']

    blocks = gen_client_level(init_data['blocks'], init_data['params']['block_demage'])

    # создаем героев
    # {'id' : player.addr[0], 'x' : player.sprite.rect.x, 'y' : player.sprite.rect.y,
    # 'team' : player.team, 'dead_count': player.config.dead_count}
    players_list = init_data['players']
    for player_item in players_list:
        x = player_item['x']
        y = player_item['y']
        id = player_item['id']
        team = player_item['team']
        dead_count = player_item['dead_count']
        tank_config = Tank_config(x, y, dead_count)
        player = Tank(tank_config, id, team)
        players.add(player)
        if id == my_id:
            i_am = player

    #создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height, WINDOW_W, WINDOW_H)

    # таймер
    timer = pygame.time.Clock()

    # надпись
    font = pygame.font.Font('freesansbold.ttf', 12)

    dropped_frames = 0
    empty_queue = 0

    # Основной цикл программы
    while 1:

        if game_client.socket._closed:
            #pygame.quit()
            return

        timer.tick(FRAME_RATE) # таймер на 30 кадров

        # отправляем произошедшие события на сервер
        event_queue = []
        for e in pygame.event.get():
            # выход
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                #pygame.quit()
                # упаковываем данные
                message = pack_data("exit")
                game_client.obuffer = message
                game_client.close()
                return

            # нажатие клавиши на клавиатуре
            if (e.type == pygame.KEYDOWN) or (e.type == pygame.KEYUP):
                event_item = {'type': e.type, 'key': e.key}
                event_queue.append(event_item)

        # упаковываем данные
        message = pack_data(event_queue)
        game_client.obuffer = message

        # получаем очередной пакет данных
        l = len(game_client.imes)
        if l > 0:
            if l > MAX_LEN_QUEUE:
                game_client.imes = game_client.imes[-MAX_LEN_QUEUE:]
                dropped_frames += (l - 3)
            dataframe = game_client.imes.pop(0)
        else:
            dataframe = {'blocks': [], 'players': [], 'bullets': []}
            empty_queue += 1

        #блоки dataframe["blocks"] = {"id" : b.id, "shootdirection" : b.shootdirection}
        blocks_list = dataframe['blocks']
        for block_data in blocks_list:
            for block in blocks.sprites():
                if block.id == block_data['id']:
                    block.die(block_data['shootdirection'])
                    break

        # игроки dataframe["players"] = { "id": player.addr[0], "x": player.sprite.rect.x, "y": player.sprite.rect.y,
        #                                 "course": player.sprite.course, "shutdirection": player.sprite.shutdirection,
        #                                 "dead": player.sprite.dead}
        players_list = dataframe['players']
        for player_item in players_list:
            for player in players.sprites():
                if player.id == player_item['id']:
                    player.update(player_item['x'], player_item['y'],
                                  player_item['course'], player_item['shutdirection'], player_item['dead'])
                    break

        # пули
        #{'id': b.id, 'x': b.rect.x, 'y': b.rect.y, 'shutdirection' : b.shutdirection, 'bum': b.bum}
        bullets_list = dataframe['bullets']
        for bullet_item in bullets_list:
            id = bullet_item['id']
            x = bullet_item['x']
            y = bullet_item['y']
            shutdirection = bullet_item['shutdirection']
            bum = bullet_item['bum']
            found = False
            for b in players_bullets.sprites():
                if b.id == id:
                    found = True
                    b.update(x, y, bum)
                    break
            if not found:
                b = Bullet(id, x, y, shutdirection)
                players_bullets.add(b)

        camera.update(i_am, WINDOW_W, WINDOW_H) # центризируем камеру относительно персонажа

        # Каждую итерацию необходимо всё перерисовывать
        screen.blit(bg, (0,0))

        # рисование блоков
        entities = blocks.sprites()
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # рисование танков
        entities = players.sprites()
        for e in entities:
            topleft = camera.apply(e)
            screen.blit(e.image, topleft)
            screen.blit(e.label, (topleft[0], topleft[1]+28))

        # рисование пуль
        entities = players_bullets.sprites()
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # выводим строчку с инфой
        label = font.render(' fps=%.2f, len_queue=%d, dropped_frames=%d, empty_queue=%d ' % (timer.get_fps(), len(game_client.imes), dropped_frames, empty_queue), True, (255,255,255), (0,0,0))
        screen.blit(label, (1, 1))

        # обновление и вывод всех изменений на экран
        pygame.display.update()

#client_main(background, screen, WINDOW_W, WINDOW_H, SERVER_ADDR, SERVER_PORT_DISP, player_name)
