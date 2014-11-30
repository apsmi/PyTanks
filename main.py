# -*- coding: utf-8 -*-
__author__ = 'apsmi'

from kivy.app import App

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image

from main_loop import PyTanksGame

from bullet import Bullet

#размеры окна, когда будем собирать андроид-пакет - убрать
#from kivy.config import Config
#width = 800
#height = 480
#Config.set('graphics', 'width', width)
#Config.set('graphics', 'height', height)


class Joystic(Widget):

    def __init__(self, size):
        self.texture_up = Image('controls/control_up.png').texture
        self.texture_down = Image('controls/control_down.png').texture
        self.texture_left = Image('controls/control_left.png').texture
        self.texture_right = Image('controls/control_right.png').texture
        self.texture = Image('controls/control.png').texture
        self.start = 2  # смещение относительно левого нижнего угла окна

        Widget.__init__(self, pos=(self.start, self.start), size=(size, size))
        with self.canvas:
            self.rectangle = Rectangle(pos=(self.start, self.start), texture=self.texture, size=self.size)

    def update(self, touch):
        # left\up or right\down
        if touch.x < touch.y :
            # left or up
            if touch.y > self.width + 2*self.start - touch.x:
                # up
                self.parent.game.player.course = "up"
                self.rectangle.texture = self.texture_up
            else:
                # left
                self.parent.game.player.course = "left"
                self.rectangle.texture = self.texture_left
        else:
            # right or down
            if touch.y > self.width + 2*self.start - touch.x:
                # right
                self.parent.game.player.course = "right"
                self.rectangle.texture = self.texture_right
            else:
                # down
                self.parent.game.player.course = "down"
                self.rectangle.texture = self.texture_down

    def on_touch_down(self, touch):
        # если попали нажатием в джойстик (х^2 + y^2 <= r^2)
        test = (touch.x - self.start - self.width/2)*(touch.x - self.start - self.height/2) +\
               (touch.y - self.start - self.width/2)*(touch.y - self.start - self.height/2)
        if test <= (self.width * self.height / 4):
            touch.grab(self)  # джойстик будет следить только за этим touch'ем
            self.update(touch)

    def on_touch_move(self, touch):
        # если это отслеживаемый touch, то поворачиваем
        if touch.grab_current is self:
            self.update(touch)

        # если это не отслеживаемый touch ...
        else:

            # проверяем, зашли в джойстик или нет
            test = (touch.x - self.start - self.width/2)*(touch.x - self.start - self.height/2) +\
                   (touch.y - self.start - self.width/2)*(touch.y - self.start - self.height/2)
            if test <= (self.width * self.height / 4):

                # если зашли, начинаем двигать танк и отслеживать touch
                touch.grab(self)
                self.update(touch)

    def on_touch_up(self, touch):
        # если это отслеживаемый джойстиком touch, тормозим танк и перестаем отслеживать touch
        if touch.grab_current is self:
            self.parent.game.player.course = ""
            self.rectangle.texture = self.texture
            touch.ungrab(self)


class MyPaintApp(App):

    def build(self):

        # Корневой виджет
        size = Window.size
        root = Widget(size=size)

        # основной объект игры
        root.game = PyTanksGame(size=root.size, pos=(0, 0))
        root.add_widget(root.game)

        # инициализация игры
        root.game.prepare()

        # Кнопка выстрела. Размер кнопки - 1/6 ширины
        control_size = min(max(root.height/3, 150), 300)
        fire_btn = Button(background_normal='controls/fire_normal.png',
                          background_down='controls/fire_press.png',
                          size=(control_size, control_size))
        fire_btn.pos = (root.width - fire_btn.width, 0)

        # выводим на окно
        root.add_widget(fire_btn)

        # обработчик событий нажатия на кнопку
        def fire_button_press(obj):

            # если у стреляющего нет пули, то стреляем
            if root.game.player.isBullet is False:

                    # создаем виджет пули
                    player_bullet = Bullet(root.game.player.x, root.game.player.y, root.game.player.shutdirection)

                    # говорим пуле чья она
                    player_bullet.shooter = root.game.player

                    # добавляем виджет пули на основное окно
                    root.game.add_widget(player_bullet)

                    # добавляем пулю в массив пуль игроков
                    player_bullet.list = root.game.players_bullets
                    root.game.players_bullets.append(player_bullet)

                    # флаг существования пули у выстрелившего игрока
                    root.game.player.isBullet = True

        # биндим обработчик
        fire_btn.bind(on_press=fire_button_press)

        # Виджет джойстика управления. Размер 1/3 меньшей стороны экрана (высоты).
        joystic = Joystic(control_size)
        root.add_widget(joystic)

        # отпустили кнопку
        #def fire_button_release(obj):
            #pass
        #fire_btn.bind(on_release=fire_button_release)

        # для вывода FPS
        label_backgroud = Widget(pos=(0, root.height-32), size=(root.width, 64))
        with label_backgroud.canvas:
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=label_backgroud.pos, size=label_backgroud.size)
        root.add_widget(label_backgroud)
        root.game.label = Label(pos=(size[0]/2, root.height-64))
        root.add_widget(root.game.label)

        # по таймеру запускаем основной цикл игры
        Clock.schedule_interval(root.game.update, 1.0 / 60.0)
        return root

if __name__ == '__main__':
    MyPaintApp().run()