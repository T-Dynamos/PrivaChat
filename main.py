from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivymd.uix.templates import RotateWidget
from kivymd.uix.button import *
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.relativelayout import *
from kivymd.toast import toast as Toast2
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from datetime import datetime
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


def Toast1(string,*largs):
    Toast2(str(string))

def Toast(string,*largs):
    if platform=="android":
        Toast2(string,gravity=80)
    else:
        Clock.schedule_once(partial(Toast1,string))

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
    server_running = False
    dialog = MDDialog

    ChatText = ChatText
    Toast = Toast

    date = lambda self: datetime.now().strftime("%H:%M:%S")
    nickname = ""
    chat_length = 40

    title = "PrivaChat (Running)"
    icon = "splash.png"


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
        Clock.schedule_once(self.load_files,2)

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


    def animate_pos_hint(self,instance,pos_hint,md_bg_color=None,radius=None):
        anim = Animation(
            md_bg_color=md_bg_color,
            pos_hint=pos_hint,
            radius=radius,
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

    def change_size_keyboard(self,instance):
        if platform == "android":
            from kvdroid.tools import keyboard_height
            if instance.size[-1] != self.y-keyboard_height():
                anim = Animation(
                    size=[self.x,self.y-keyboard_height()],
                    d=0.2
                    )
                anim.start(instance)
            else:
                anim = Anibmation(
                    size=[self.x,self.y],
                    d=0.2
                    )
                anim.start(instance)
        else:
            pass

    def connect_client(self,addr,nickname,*largs):
        self.nickname = nickname
        send_message = lambda : Clock.schedule_once(self.handle_chat)
        recieve_message = lambda  msg,nickname : Clock.schedule_once(partial(self.handle_msg,msg,nickname))
        self.client = appServer.handle_client(nickname,send_message,recieve_message,int(addr.split(":")[-1]),addr.split(":")[0],print)
        _thread.start_new_thread(self.client[-1],())
        self.chat.open()

    def handle_chat(self,*largs):
        if self.chat.ids.text_feild.text != len(self.chat.ids.text_feild.text)*" " and len(self.chat.ids.text_feild.text) < self.chat_length:
            widget = ChatText()
            widget.text = self.chat.ids.text_feild.text
            instance = self.chat.ids.chat_handler.add_widget(widget)
            self.chat.ids.view.scroll_to(widget)
            self.chat.ids.text_feild.text = " "
            return True

    def handle_msg(self,msg,nickname,*largs):
        print(msg,nickname)
        widget = PersonText()
        widget.text = msg
        widget.nickname  = nickname
        self.chat.ids.chat_handler.add_widget(widget)
        self.chat.ids.view.scroll_to(widget)

    def add_server_log(self,log):
        def add(*largs):
            label = Builder.load_string(f"""
MDLabel:
    size_hint:None,None
    size:app.x-dp(40),dp(20)
    text:"{log}"
    font_name:"assets/SourceCodePro-Regular.otf"
                """)

            self.main_screen.ids.server_loger.add_widget(label)
        Clock.schedule_once(add)

    def start_server(self,port):
        try:
            self.main_screen.ids.server_card.opacity  = 1
            _thread.start_new_thread(appServer.start_server,(int(port.text),self.add_server_log,self.stop_server))
            self.server_view.dismiss()
            self.server_running = True
            self.animate_icon(self.main_screen.ids.server_icon,"close")
            self.main_screen.ids.server_text.text  = "Stop server"
            Toast("Server started successfully")
        except Exception as e:
            Toast("Unable to start server :"+str(e))
            self.server_view.dismiss()
            port.text = ""

    def stop_server(self):
        self.dialog = MDDialog(
            title="Stop Server?",
            text="Stopping a server requires a restart.",
            radius=dp(20),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.dialog.dismiss
                        ),  
                MDFlatButton(
                    text="Restart Now",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=self.stop
                        ),
                    ],
            )
        self.dialog.open()

        #self.animate_icon(self.main_screen.ids.server_icon,"plus")
        #self.main_screen.ids.server_text.text  = "Start a server"
        #self.server_running = False
        #self.main_screen.ids.server_card.opacity  = 0
        #self.server_view.ids.test_text_feild.text = ""



PrivaChat().run()
