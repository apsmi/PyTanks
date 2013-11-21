# -*- coding: utf-8 -*-

import sys
import pygame
from pygame import *
import time

from client_level import gen_client_level
from bullet import Bullet
import client_tank# import Tank_config, Tank
from monster_config import *
from camera import  camera_configure, Camera

from monster import Monster

import asyncore, socket, asynchat, threading, pickle, struct

LEN_TERM = 4

# фиктивный диспетчер
class Fiktive_Dispatcher(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', 0))
        self.listen(1)

# сокет, принимающий соединение от клиентов
class Client(asynchat.async_chat):

    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.ibuffer = []
        self.obuffer = b""
        self.imes = [] #b""
        self.set_terminator(LEN_TERM)
        self.state = "len"

    def handle_close(self):
        print(self.socket.getsockname())
        self.close()

    def writable(self):
        return len(self.obuffer) > 0

    def handle_write(self):
        sent = self.sendto(self.obuffer, self.addr)
        self.obuffer = self.obuffer[sent:]

    def collect_incoming_data(self, data):
        self.ibuffer.append(data)

    def found_terminator(self):
        dataframe = b"".join(self.ibuffer)
        self.ibuffer = []
        if self.state == "len":
            self.state = "data"
            length = struct.unpack('L',dataframe)[0]
            self.set_terminator(length)
        elif self.state == "data":
            self.state = "len"
            self.set_terminator(LEN_TERM)
            self.imes.append(pickle.loads(dataframe))

class Socket_Loop(threading.Thread):

    def __init__(self, function, arg):
        threading.Thread.__init__(self)
        self.function = function
        self.arg = arg

    def run(self):
        self.function(self.arg)


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

def main():

    # фиктивный диспетчер
    f_d = Fiktive_Dispatcher()

    # открываем сокет TCP

    SERVER_ADDR = 'localhost'
    SERVER_PORT_TCP = 80

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDR, SERVER_PORT_TCP))

    # получем серверный udp порт
    buf = sock.recv(1024)
    server_port = struct.unpack('L',buf)[0]

    # создаем UPD сокет
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_udp.bind(('', 0))
    client_port = socket_udp.getsockname()[1]

    # отправляем порт созданного сокета серверу
    buf = struct.pack('L', client_port)
    sock.sendall(buf)
    sock.close()

    # создаем асинхронный клиент
    game_client = Client(socket_udp, (SERVER_ADDR, server_port))

    # запускаем цикл опроса сокетов
    socket_loop_thread = Socket_Loop(asyncore.loop, 0.01)
    socket_loop_thread.start()

    # Инициация PyGame, обязательная строчка
    pygame.init()
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    #  инициализация окна
    bg, screen = window_init(800, 640, "#000000", "PyTanks")

    # группы объектов
    players = pygame.sprite.Group()
    players_bullets = pygame.sprite.Group()
    #monsters = pygame.sprite.Group()
    #monsters_bullets = pygame.sprite.Group()

    # получаем первоначальную инфу
    #time.sleep(5)
    while len(game_client.imes) <= 0:
        time.sleep(1)

    init_data = game_client.imes.pop(0)

    print("Level recieved ", time.time())

    # генерируем уровень
    total_level_width = init_data['level']['total_width']
    total_level_height = init_data['level']['total_height']

    blocks = gen_client_level(init_data['blocks'])

    # создаем героев
    # {'id' : player.addr[0], 'x' : player.sprite.rect.x, 'y' : player.sprite.rect.y, 'team' : player.team}
    players_list = init_data['players']
    for player_item in players_list:
        x = player_item['x']
        y = player_item['y']
        id = player_item['id']
        team = player_item['team']
        tank_config = client_tank.Tank_config(x, y)
        player = client_tank.Tank(tank_config, id, team)
        players.add(player)
    
    #создаем камеру
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # таймер
    timer = pygame.time.Clock()

    # надпись
    font = pygame.font.Font(None, 18)

    print("starting loop")

    # Основной цикл программы
    while 1:

        timer.tick(30) # таймер на 30 кадров

        # отправляем произошедшие события на сервер
        event_queue = []
        for e in pygame.event.get():
            # выход
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # нажатие клавиши на клавиатуре
            if (e.type == KEYDOWN) or (e.type == KEYUP):
                event_item = {'type': e.type, 'key': e.key}
                event_queue.append(event_item)

        # упаковываем данные
        message = pack_data(event_queue)
        game_client.obuffer = message

        # получаем очередной пакет данных
        if len(game_client.imes) > 0:
            dataframe = game_client.imes.pop(0)
        else:
            dataframe = {'blocks': [], 'players': []}
            print("No data in pop")

        #блоки dataframe["blocks"] = {"id" : b.id, "shootdirection" : b.shootdirection}
        blocks_list = dataframe['blocks']
        for block_data in blocks_list:
            for block in blocks.sprites():
                if block.id == block_data['id']:
                    block.die(block_data['shootdirection'])

        # игроки dataframe["players"] = { "id": player.addr[0], "x": player.sprite.rect.x, "y": player.sprite.rect.y,
        #                                 "course": player.sprite.course, "shutdirection": player.sprite.shutdirection,
        #                                 "dead": player.sprite.dead}
        players_list = dataframe['players']
        for player_item in players_list:
            for player in players.sprites():
                if player.id == player_item['id']:
                    player.update(player_item['x'], player_item['y'],
                                  player_item['course'], player_item['shutdirection'], player_item['dead'])

        # обновление всех объектов
        #players.update( blocks.sprites() + monsters.sprites())
        #players_bullets.update( blocks.sprites() + monsters.sprites() + monsters_bullets.sprites())
        #monsters_bullets.update( blocks.sprites() + players.sprites() + players_bullets.sprites())
        #monsters.update( blocks.sprites() + players.sprites() + monsters.sprites(), player.rect.top, player.rect.left, monsters_bullets)
        camera.update(players.sprites()[0]) # центризируем камеру относительно персонажа

        # Каждую итерацию необходимо всё перерисовывать
        screen.blit(bg, (0,0))

        # рисование всех объектов
        entities = blocks.sprites() + players.sprites() + players_bullets.sprites()# + monsters_bullets.sprites() + monsters.sprites()
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # выводим FPS
        label = font.render(' %.2f ' % timer.get_fps(), True, (255,255,255), (0,0,0))
        screen.blit(label, (1, 1))

        # обновление и вывод всех изменений на экран
        pygame.display.update()

if __name__ == "__main__":
    main()
