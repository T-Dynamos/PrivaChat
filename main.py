from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivymd.uix.templates import RotateWidget
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import *
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import *
import socket 
import os
import select
import _thread
import appServer

__version__ = "1.0"

class IconButton(MDIconButton,RotateWidget):
    pass

class ChatText(MDRelativeLayout):
    pass

class PersonText(MDRelativeLayout):
    pass

class HoverLayout(MDCard,HoverBehavior):
    pass

class PrivaChat(MDApp):

    __version__ = __version__
    
    x = Window.size[0]
    y = Window.size[1]

    screen_manager = ScreenManager()

    server_view = None
    chat_view = None
    main_screen = None
    settings_view = None
    chat = None
    chat_img = ""

    ChatText = ChatText

    def build(self):
        self.chat_img = "/usr/share/backgrounds/hack.jpg"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.screen_manager.add_widget(Builder.load_file("kvfiles/splash.kv"))
        self.screen_manager.current = "splash"
        return self.screen_manager


    def on_start(self):
        if platform != "android":
            Window.size = [dp(400),dp(600)]
        Clock.schedule_once(self.load_files)

    def load_files(self,*largs):
        self.main_screen = Builder.load_file("main.kv")
        self.chat_view = Builder.load_file("kvfiles/chat_connect.kv")
        self.server_view = Builder.load_file("kvfiles/server_start.kv")
        self.settings_view = Builder.load_file("kvfiles/settings_view.kv")
        self.chat = Builder.load_file("kvfiles/chat.kv")        
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.transition = FadeTransition()
        self.screen_manager.current = "main"
        self.screen_manager.transition = SlideTransition()


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
 
    def animate_md_bg_color(self,instance,md_bg_color=None):
        anim = Animation(
            md_bg_color=md_bg_color,
            d= 0.3
            )
        anim.start(instance)

    def open_modal(self,instance):
    	anim = Animation(
                opacity=1,
                d=0.3
                ).start(instance)

    def close_modal(self,instance):
    	anim = Animation(
                opacity=0,
                d=0.3
                ).start(instance)

    def open_drawer(self,*largs):
        animation_open = Animation(
                pos_hint={"center_x":0.5,"center_y":0.5},
                d=0.2
               )
        animation_close = Animation(
                pos_hint={"center_x":-0.5,"center_y":0.5},
                d=0.2
                )
        if self.screen_manager.get_screen("main").ids.drawer.pos_hint == {"center_x":-0.5,"center_y":0.5}:
            animation_open.start(self.screen_manager.get_screen("main").ids.drawer) 
            def set_opacity(*largs):
                self.screen_manager.get_screen("main").ids.drawer.md_bg_color = 0,0,0,.3

            animation_open.bind(on_complete=set_opacity)
        else:
            self.screen_manager.get_screen("main").ids.drawer.md_bg_color  = 0,0,0,0
            animation_close.start(self.screen_manager.get_screen("main").ids.drawer)
            Clock.schedule_once(partial(self.animate_icon,self.screen_manager.get_screen("main").ids.back_button,"menu" if self.icon == "arrow-left" else "menu" ),0.1)

    def handle_chat(self,instance,grid,view):
        if instance.text != " ":
            grid.add_widget(ChatText(text=instance.text))
            view.scroll_to(instance)
            instance.text = ""

PrivaChat().run()
