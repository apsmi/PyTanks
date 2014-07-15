# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle

from kivy.clock import Clock

from pygame.sprite import Group

from level import gen_level
from tank import Tank, TankWidget
from monster_config import *
from camera import camera_configure, Camera
from monster import Monster


class PyTanksGame(Widget):

    def prepare(self):

        self.dt = 0  # дельта времени вызова update()
        self.dt_anim = 0
        self.anim = False  # индикатор анимации

        # группы объектов
        #self.players = Group()
        #self.players_bullets = Group()
        #self.monsters = Group()
        #self.monsters_bullets = Group()
        #self.blocks = Group()
        # группы объектов
        self.players = []
        self.players_bullets = []
        self.monsters = []
        self.monsters_bullets = []
        self.blocks = []

        # создаем героя
        #player_config = Tank_config()
        #self.player = Tank(player_config)
        #self.players.add(self.player)
        # создаем героя
        self.player = TankWidget()
        self.players.append(self.player)
        self.add_widget(self.player)

        # TODO: переписать монстров на виджеты

        # монстр 1
        #monster_config = Monster_config_1()
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # монстр 2
        #monster_config = Monster_config_2()
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # монстр 3
        #monster_config = Monster_config_3()
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # генерируем уровень
        self.blocks, total_level_width, total_level_height = gen_level(50, 50)

        # добавляем виджеты блоков
        for item in self.blocks:
            self.add_widget(item)

        #создаем камеру
            #display_w, display_h = self.width, self.height
        #self.camera = Camera(camera_configure, total_level_width, total_level_height, display_w, display_h)

        # рисуем все объекты
        #with self.canvas:
            #for item in self.players.sprites() + self.monsters.sprites() + self.blocks.sprites():
                #item.picture = Rectangle(texture=item.texture, pos=(item.rect.x, item.rect.y),
                                         #size=item.texture.size)

    def update(self, dt):

        text = "clock-fps: %f | clock-rfps: %f" % (Clock.get_fps(), Clock.get_rfps())
        self.label.text = text

        # таймер анимации
        self.dt_anim += dt
        if self.dt_anim > 0.1:
            self.anim = not self.anim
            self.dt_anim = 0

        # таймер симуляции мира
        self.dt += dt
        if self.dt > (1.0/30.0):
            self.dt = 0

            # симуляция мира
            #self.player.update(self.blocks.sprites() + self.monsters.sprites(), self.anim)
            #self.players_bullets.update(self.blocks.sprites() + self.monsters.sprites() + self.monsters_bullets.sprites(), self.anim)
            #self.monsters_bullets.update(self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites(), self.anim)
            #self.monsters.update(self.blocks.sprites() + self.players.sprites() + self.monsters.sprites(),
                                 #self.player.rect.top, self.player.rect.left, self.monsters_bullets, self.anim, self.canvas)

            self.player.update(self.blocks + self.monsters, self.anim)

            #self.camera.update(self.player)  # центризируем камеру относительно персонажа

            # Каждую итерацию необходимо всё перерисовывать
            #self.canvas.clear()

            # рисование всех объектов
            #entities = self.players.sprites() + self.players_bullets.sprites() + self.monsters_bullets.sprites() +\
                #self.monsters.sprites() + self.blocks.sprites()
            #for e in entities:
                #pos = self.camera.apply(e)
                #e.picture.texture = e.texture
                #e.picture.pos = (pos.x, pos.y)
                #e.picture.size = e.texture.size