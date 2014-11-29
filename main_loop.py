# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget

from kivy.clock import Clock

from level import gen_level
from tank import TankWidget
from camera import NewCamera
from monster import Monster1


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
        #monster_item = Monster1()
        #self.monsters.append(monster_item)
        #self.add_widget(monster_item)

        # монстр 2
        #monster_config = Monster_config_2()
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # монстр 3
        #monster_config = Monster_config_3()
        #monster = Monster(monster_config)
        #self.monsters.add(monster)

        # генерируем уровень
        l_w = self.width / 32 + 10
        l_h = self.height / 32 + 10
        self.blocks, total_level_width, total_level_height = gen_level(l_h, l_w)

        # добавляем виджеты блоков
        for item in self.blocks:
            self.add_widget(item)

        #создаем камеру
        display_w, display_h = self.width, self.height
        self.camera = NewCamera(total_level_width, total_level_height, display_w, display_h)

        # рисуем все объекты
        #with self.canvas:
            #for item in self.players.sprites() + self.monsters.sprites() + self.blocks.sprites():
                #item.picture = Rectangle(texture=item.texture, pos=(item.rect.x, item.rect.y),
                                         #size=item.texture.size)

    def update(self, dt):

        text = "clock-fps: %f | clock-rfps: %d" % (Clock.get_fps(), Clock.get_rfps())
        self.label.text = text + " /// " + str(self.label.s)

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

            self.player.update(self.blocks + self.monsters, self.anim)
            #self.players_bullets.update(self.blocks.sprites() + self.monsters.sprites() + self.monsters_bullets.sprites(), self.anim)
            #self.monsters_bullets.update(self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites(), self.anim)
            for m in self.monsters:
                m.update(self.blocks + self.players + self.monsters, self.player.y, self.player.x,
                         self.monsters_bullets, self.anim, self.canvas)

            self.camera.update(self.player)  # центризируем камеру относительно персонажа

            # рисование всех объектов
            entities = self.players + self.players_bullets + self.monsters_bullets + self.monsters + self.blocks
            for e in entities:
                pos = self.camera.apply(e)
                e.rectangle.pos = pos