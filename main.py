# -*- coding: utf-8 -*-
__author__ = 'apsmi'

from kivy.app import App

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle

from main_loop import PyTanksGame

from bullet import Bullet

#размеры окна, когда будем собирать андроид-пакет - убрать
from kivy.config import Config
width = 800
height = 480
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)


class MyPaintApp(App):

    def build(self):

        # Корневой виджет, основной объект игры
        size = Window.size
        parent = Widget(size=size)  # size=size
        parent.game = PyTanksGame(size=parent.size, pos=(0, 0))
        parent.game.prepare()
        parent.add_widget(parent.game)

        #кнопки
        right_btn = Button(background_normal='controls/right_normal.png',
                           background_down='controls/right_press.png',
                           pos=(size[0]/3, size[1]/8), size=(size[1]/4, size[1]/4))
        left_btn = Button(background_normal='controls/left_normal.png',
                          background_down='controls/left_press.png',
                          pos=(0, size[1]/8), size=(size[1]/4, size[1]/4))
        up_btn = Button(background_normal='controls/up_normal.png',
                        background_down='controls/up_press.png',
                        pos=(size[0]/6, size[1]/4), size=(size[1]/4, size[1]/4))
        down_btn = Button(background_normal='controls/down_normal.png',
                          background_down='controls/down_press.png',
                          pos=(size[0]/6, 0), size=(size[1]/4, size[1]/4))
        fire_btn = Button(background_normal='controls/fire_normal.png',
                          background_down='controls/fire_press.png',
                          pos=(size[0]-size[0]/6, size[1]/8), size=(size[1]/4, size[1]/4))

        parent.game.label = Label(pos=(100, size[1] - 100))  # для вывода FPS
        parent.game.label.size = size
        parent.add_widget(parent.game.label)

        #добавляем кнопки на корневой виджет
        parent.add_widget(right_btn)
        parent.add_widget(left_btn)
        parent.add_widget(up_btn)
        parent.add_widget(down_btn)
        parent.add_widget(fire_btn)

        #обработчики событий нажатия на кнопки
        def fire_button_press(obj):
            pass  # TODO: переписать пули на виджеты
            #if parent.game.player.isBullet is False:
                    #player_bullet = Bullet(parent.game.player.rect.left, parent.game.player.rect.top, parent.game.player.shutdirection)
                    #player_bullet.shooter = parent.game.player
                    #with parent.game.canvas:
                        #player_bullet.picture = Rectangle(texture=player_bullet.texture,
                                                          #pos=(player_bullet.rect.x, player_bullet.rect.y),
                                                          #size=player_bullet.texture.size)
                    #parent.game.players_bullets.add(player_bullet)
                    #parent.game.player.isBullet = True
        fire_btn.bind(on_press=fire_button_press)

        def up_button_press(obj):
            parent.game.player.course = "up"
        up_btn.bind(on_press=up_button_press)

        def down_button_press(obj):
            parent.game.player.course = "down"
        down_btn.bind(on_press=down_button_press)

        def left_button_press(obj):
            parent.game.player.course = "left"
        left_btn.bind(on_press=left_button_press)

        def right_button_press(obj):
            parent.game.player.course = "right"
        right_btn.bind(on_press=right_button_press)

        # отпустили кнопку
        def fire_button_release(obj):
            pass
        fire_btn.bind(on_release=fire_button_release)

        def up_button_release(obj):
            parent.game.player.course = ""
        up_btn.bind(on_release=up_button_release)

        def down_button_release(obj):
            parent.game.player.course = ""
        down_btn.bind(on_release=down_button_release)

        def left_button_release(obj):
            parent.game.player.course = ""
        left_btn.bind(on_release=left_button_release)

        def right_button_release(obj):
            parent.game.player.course = ""
        right_btn.bind(on_release=right_button_release)

        Clock.schedule_interval(parent.game.update, 1.0 / 60.0)
        return parent

if __name__ == '__main__':
    MyPaintApp().run()