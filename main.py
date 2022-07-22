from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivymd.uix.templates import RotateWidget
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from kivy.clock import Clock
from kivy.animation import Animation
import socket 
import os
import select 
import _thread

__version__ = "1.0"

class IconButton(MDIconButton,RotateWidget):
    pass

class HoverLayout(MDCard,HoverBehavior):
    pass

class PrivaChat(MDApp):

    __version__ = __version__
    x = Window.size[0]
    y = Window.size[1]

    def build(self):
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        return Builder.load_file("main.kv")

    def on_start(self):
        if platform != "android":
            Window.size = [dp(400),dp(600)]

    def animate_icon(self,instance,icon,*largs):
        
        anim = Animation(
            rotate_value_angle=-360, 
            d=0.3
                )

        anim2 = Animation(
            opacity=0,
            d=0.4
                )

        anim.start(instance)

        def change_icon(*largs):

            instance.icon = icon 
            instance.opacity = 1
            instance.rotate_value_angle = 1
            anim2.start(instance)

        anim2.start(instance)
        anim2.bind(on_complete=change_icon)

    def animate_pos_hint(self,instance,pos_hint,md_bg_color=None):
        anim = Animation(
            md_bg_color=md_bg_color,
            pos_hint=pos_hint,
            d= 0.3
            )
        anim.start(instance)
    def open_drawer(self,*largs):
        animation_open = Animation(
                pos_hint={"center_x":0.5,"center_y":0.5},
                d=0.2
               )
        animation_close = Animation(
                pos_hint={"center_x":-0.5,"center_y":0.5},
                d=0.2
                )
        if self.root.ids.drawer.pos_hint == {"center_x":-0.5,"center_y":0.5}:
            animation_open.start(self.root.ids.drawer) 
            def set_opacity(*largs):
                self.root.ids.drawer.md_bg_color = 0,0,0,.3

            animation_open.bind(on_complete=set_opacity)
        else:
            self.root.ids.drawer.md_bg_color  = 0,0,0,0
            animation_close.start(self.root.ids.drawer)


PrivaChat().run()
