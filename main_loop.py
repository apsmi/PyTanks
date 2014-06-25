# -*- coding: utf-8 -*-
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle

from pygame.sprite import Group

from level import gen_level
from tank import Tank_config, Tank
from monster_config import *
from camera import  camera_configure, Camera
from monster import Monster



class PyTanksGame(Widget):

    def prepare(self):

        # группы объектов
        self.players = Group()
        self.players_bullets = Group()
        self.monsters = Group()
        self.monsters_bullets = Group() # перемещено в глобальную переменную

        # создаем героя
        player_config = Tank_config()
        self.player = Tank(player_config)
        self.players.add(self.player)

        # монстр 1
        #monster_config = Monster_config_1(100, 100)
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # монстр 1
        #monster_config = Monster_config_2(200, 200)
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # монстр 1
        #monster_config = Monster_config_3(300, 300)
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # генерируем уровень
        self.blocks, total_level_width, total_level_height = gen_level(25,25)

        display_w, display_h = self.width, self.height

        #создаем камеру
        self.camera = Camera(camera_configure, total_level_width, total_level_height, display_w, display_h)

    def update(self, dt):

        # симуляция мира
        self.players.update(self.blocks.sprites() + self.monsters.sprites())
        self.players_bullets.update(self.blocks.sprites() + self.monsters.sprites() + self.monsters_bullets.sprites())
        self.monsters_bullets.update(self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites())
        self.monsters.update(self.blocks.sprites() + self.players.sprites() + self.monsters.sprites(),
                             self.player.rect.top, self.player.rect.left, self.monsters_bullets)

        self.camera.update(self.player)  # центризируем камеру относительно персонажа

        # Каждую итерацию необходимо всё перерисовывать
        self.canvas.clear()

        # рисование всех объектов
        entities = self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites() + \
                   self.monsters_bullets.sprites() + self.monsters.sprites()
        for e in entities:
            with self.canvas:
                pos = self.camera.apply(e)
                Rectangle(texture=e.texture, pos=(pos.x, self.height - pos.y - 32), size=e.texture.size)