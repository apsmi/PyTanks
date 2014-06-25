# -*- coding: utf-8 -*-
__author__ = 'master'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Rectangle

from main_loop import main_loop_prepare, main_loop
from bullet import Bullet

#размеры окна, когда будем собирать андроид-пакет - убрать
width = 800
height = 480
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)


class MyPaintApp(App):

    def __init__(self):
        self.size = (640, 480)
        self.painter = None
        self.player, self.players_bullets, self.players, self.blocks, self.monsters, \
            self.monsters_bullets, self.camera = main_loop_prepare()
        App.__init__(self)

    def update(self):

        # симуляция мира
        self.players.update(self.blocks.sprites() + self.monsters.sprites())
        self.players_bullets.update(self.blocks.sprites() + self.monsters.sprites() + self.monsters_bullets.sprites())
        self.monsters_bullets.update(self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites())
        self.monsters.update(self.blocks.sprites() + self.players.sprites() + self.monsters.sprites(),
                             self.player.rect.top, self.player.rect.left, self.monsters_bullets)

        self.camera.update(self.player)  # центризируем камеру относительно персонажа

        # Каждую итерацию необходимо всё перерисовывать
        self.painter.canvas.clear()

        # рисование всех объектов
        entities = self.blocks.sprites() + self.players.sprites() + self.players_bullets.sprites() + \
                   self.monsters_bullets.sprites() + self.monsters.sprites()
        for e in entities:
            with self.painter.canvas:
                Rectangle(texture=e.texture, pos=self.camera.apply(e), size=e.size)

    def build(self):

        parent = Widget(size=(width, height))  # родительский, НЕ root  !!!!!!!!!!   УБРАТЬ РАЗМЕР ДЛЯ АНДРОИДА
        self.size = parent.size

        self.painter = Widget(size=self.size)   # на нем будем рисовать

        #кнопки
        right_btn = Button(background_normal='controls/right_normal.png', background_down='controls/right_press.png',
                           pos=(160, 80))
        left_btn = Button(background_normal='controls/left_normal.png', background_down='controls/left_press.png',
                          pos=(0, 80))
        up_btn = Button(background_normal='controls/up_normal.png', background_down='controls/up_press.png',
                        pos=(80, 160))
        down_btn = Button(background_normal='controls/down_normal.png', background_down='controls/down_press.png',
                          pos=(80, 0))
        fire_btn = Button(background_normal='controls/fire_normal.png', background_down='controls/fire_press.png',
                          pos=(width-140, 40))

        #добавляем кнопки на родительский
        parent.add_widget(self.painter)
        parent.add_widget(right_btn)
        parent.add_widget(left_btn)
        parent.add_widget(up_btn)
        parent.add_widget(down_btn)
        parent.add_widget(fire_btn)

        #обработчики событий нажатия на кнопки
        def fire_button_press(obj):
            if self.player.isBullet:
                    self.player_bullet = Bullet(self.player.rect.left, self.player.rect.top, self.player.shutdirection)
                    self.player_bullet.shooter = self.player
                    self.players_bullets.add(self.player_bullet)
                    self.player.isBullet = True
        fire_btn.bind(on_press=fire_button_press)

        def up_button_press(obj):
            self.player.course = "up"
        up_btn.bind(on_press=up_button_press)

        def down_button_press(obj):
            self.player.course = "down"
        down_btn.bind(on_press=down_button_press)

        def left_button_press(obj):
            self.player.course = "left"
        left_btn.bind(on_press=left_button_press)

        def right_button_press(obj):
            self.player.course = "right"
        right_btn.bind(on_press=right_button_press)

        # отпустили кнопку
        def fire_button_release(obj):
            pass
        fire_btn.bind(on_release=fire_button_release)

        def up_button_release(obj):
            self.player.course = ""
        up_btn.bind(on_release=up_button_release)

        def down_button_release(obj):
            self.player.course = ""
        down_btn.bind(on_release=down_button_release)

        def left_button_release(obj):
            self.player.course = ""
        left_btn.bind(on_release=left_button_release)

        def right_button_release(obj):
            self.player.course = ""
        right_btn.bind(on_release=right_button_release)


        Clock.schedule_interval(self.update, 1.0 / 60.0)


        return parent


if __name__ == '__main__':
    MyPaintApp().run()