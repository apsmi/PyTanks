# -*- coding: utf-8 -*-
__author__ = 'master'

from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from main_loop import PyTanksGame
from bullet import Bullet

#размеры окна, когда будем собирать андроид-пакет - убрать
#width = 800
#height = 480
#Config.set('graphics', 'width', width)
#Config.set('graphics', 'height', height)


class MyPaintApp(App):

    def build(self):
        size = Window.size
        parent = Widget(size=size)  #
        game = PyTanksGame(size=parent.size, pos=(0, 0))
        game.prepare()

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
                          pos=(parent.width-140, 40))

        #добавляем кнопки на родительский
        parent.add_widget(game)
        parent.add_widget(right_btn)
        parent.add_widget(left_btn)
        parent.add_widget(up_btn)
        parent.add_widget(down_btn)
        parent.add_widget(fire_btn)

        #обработчики событий нажатия на кнопки
        def fire_button_press(obj):
            if game.player.isBullet:
                    game.player_bullet = Bullet(game.player.rect.left, game.player.rect.top, game.player.shutdirection)
                    game.player_bullet.shooter = game.player
                    game.players_bullets.add(game.player_bullet)
                    game.player.isBullet = True
        fire_btn.bind(on_press=fire_button_press)

        def up_button_press(obj):
            game.player.course = "up"
        up_btn.bind(on_press=up_button_press)

        def down_button_press(obj):
            game.player.course = "down"
        down_btn.bind(on_press=down_button_press)

        def left_button_press(obj):
            game.player.course = "left"
        left_btn.bind(on_press=left_button_press)

        def right_button_press(obj):
            game.player.course = "right"
        right_btn.bind(on_press=right_button_press)

        # отпустили кнопку
        def fire_button_release(obj):
            pass
        fire_btn.bind(on_release=fire_button_release)

        def up_button_release(obj):
            game.player.course = ""
        up_btn.bind(on_release=up_button_release)

        def down_button_release(obj):
            game.player.course = ""
        down_btn.bind(on_release=down_button_release)

        def left_button_release(obj):
            game.player.course = ""
        left_btn.bind(on_release=left_button_release)

        def right_button_release(obj):
            game.player.course = ""
        right_btn.bind(on_release=right_button_release)

        parent.game = game
        Clock.schedule_interval(parent.game.update, 1.0 / 60.0)
        return parent

if __name__ == '__main__':
    MyPaintApp().run()