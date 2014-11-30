# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget

from kivy.clock import Clock

from level import gen_level
from tank import Player
from camera import NewCamera
from monster import Monster1, Monster2, Monster3
from bullet import Bullet


class PyTanksGame(Widget):

    def prepare(self):

        self.dt = 0  # дельта времени вызова update()
        self.dt_anim = 0
        self.anim = False  # индикатор анимации

        # группы объектов
        self.players = []
        self.players_bullets = []
        self.monsters = []
        self.monsters_bullets = []
        self.blocks = []

        # создаем героя
        self.player = Player()
        self.players.append(self.player)
        self.add_widget(self.player)

        # монстр 1
        monster_item = Monster1()
        self.monsters.append(monster_item)
        self.add_widget(monster_item)

        # монстр 2
        monster_item = Monster2()
        self.monsters.append(monster_item)
        self.add_widget(monster_item)

        # монстр 3
        monster_item = Monster3()
        self.monsters.append(monster_item)
        self.add_widget(monster_item)

        # генерируем уровень
        l_w = self.width / 32 + 5
        l_h = self.height / 32 + 5
        self.blocks, total_level_width, total_level_height = gen_level(l_h, l_w)
        total_level_height += 32  # место под посказки сверху

        # добавляем виджеты блоков
        for item in self.blocks:
            self.add_widget(item)

        # создаем камеру
        display_w, display_h = self.width, self.height
        self.camera = NewCamera(total_level_width, total_level_height, display_w, display_h)

    def update(self, dt):

        text = "clock-fps: %f | clock-rfps: %d" % (Clock.get_fps(), Clock.get_rfps())
        self.label.text = text + " /// " + str(self.size)

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
            for item in self.children:
                # игроки
                if isinstance(item, Player):
                    item.update(self.blocks + self.monsters, self.anim)

                # пули игроков
                if isinstance(item, Bullet) and isinstance(item.shooter, Player):
                    item.update(self.blocks + self.monsters + self.monsters_bullets, self.anim)

                # пули монстров
                if isinstance(item, Bullet) and isinstance(item.shooter, (Monster1, Monster2, Monster3)):
                    item.update(self.blocks + self.players + self.players_bullets, self.anim)

                # монстры
                if isinstance(item, (Monster1, Monster2, Monster3)):
                    item.update(self.blocks + self.players + self.monsters, self.player.y, self.player.x, self.anim)

            self.camera.update(self.player)  # центризируем камеру относительно персонажа

            # рисование всех объектов относительно камеры
            for e in self.children:
                pos = self.camera.apply(e)
                e.rectangle.pos = pos