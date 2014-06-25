__author__ = 'master'
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.config import Config

#размеры окна, когда будем собирать андроид-пакет - убрать
width = 800
height = 480
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)

class MyPaintApp(App):

    def build(self):
        parent = Widget(size=(width,height)) #родительский, НЕ root  !!!!!!!!!!   УБРАТЬ РАЗМЕР ДЛЯ АНДРОИДА
        painter = Widget(size=parent.size)   #на нем будем рисовать

        #кнопки
        right_btn = Button(background_normal='controls/right_normal.png', background_down='controls/right_press.png', pos=(160, 80))
        left_btn = Button(background_normal='controls/left_normal.png', background_down='controls/left_press.png', pos=(0, 80))
        up_btn = Button(background_normal='controls/up_normal.png', background_down='controls/up_press.png', pos=(80, 160))
        down_btn = Button(background_normal='controls/down_normal.png', background_down='controls/down_press.png', pos=(80, 0))
        fire_btn = Button(background_normal='controls/fire_normal.png', background_down='controls/fire_press.png', pos=(width-140, 40))

        #добавляем кнопки на родительский
        parent.add_widget(painter)
        parent.add_widget(right_btn)
        parent.add_widget(left_btn)
        parent.add_widget(up_btn)
        parent.add_widget(down_btn)
        parent.add_widget(fire_btn)

        #обработчики событий нажатия на кнопки
        def fire_buttton_press(obj):
            pass
        fire_btn.bind(on_release=fire_buttton_press)

        def up_buttton_press(obj):
             pass
        up_btn.bind(on_release=up_buttton_press)

        def down_buttton_press(obj):
            pass
        down_btn.bind(on_release=down_buttton_press)

        def left_buttton_press(obj):
             pass
        left_btn.bind(on_release=left_buttton_press)

        def right_buttton_press(obj):
             pass
        right_btn.bind(on_release=right_buttton_press)

        return parent


if __name__ == '__main__':
    MyPaint = MyPaintApp()
    MyPaint.run()