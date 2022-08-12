from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivymd.uix.templates import RotateWidget
from kivymd.uix.button import *
from kivymd.uix.dialog import MDDialog
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast as Toast2
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform
from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.config import Config
from datetime import datetime
from kivy.uix.screenmanager import *
import _thread
import appServer
import os

__version__ = "1.0"

if platform != "android":
    Config.set("graphics", "height", "600")
    Config.set("graphics", "width", "400")
    Config.set("graphics", "fps", "120")
    Window.size = [dp(400), dp(600)]

Config.set("kivy", "exit_on_escape", "0")


class IconButton(MDIconButton, RotateWidget):
    pass


class ChatText(MDRelativeLayout):
    pass


class PersonText(MDRelativeLayout):
    pass


class HoverLayout(MDCard, HoverBehavior):
    pass


class ImgBox(MDBoxLayout):
    pass


def Toast1(string, *largs):
    Toast2(str(string))


def Toast(string, *largs):
    if platform == "android":
        Toast2(string, gravity=80)
    else:
        Clock.schedule_once(partial(Toast1, string))


class PrivaChat(MDApp):
    __version__ = __version__

    x = lambda self: Window.size[0]
    y = lambda self: Window.size[1]

    screen_manager = ScreenManager()

    server_view = None
    chat_view = None
    main_screen = None
    settings_view = None
    chat = None
    wall_change = None
    chat_img = ""
    server_running = False
    dialog = MDDialog

    ChatText = ChatText
    Toast = Toast

    date = lambda self: datetime.now().strftime("%H:%M:%S")
    nickname = ""
    chat_length = 1000
    text_size = None

    title = "PrivaChat (Running)"
    icon = "splash.png"

    back_key = 27

    MDLabel = MDLabel

    def open_wall(self):
        for file in os.listdir("wallpapers"):
            widget = ImgBox()
            widget.img = "wallpapers/"+file
            self.wall_change.ids.wall_box.add_widget(widget)
        self.wall_change.open()

    def ch_s(self,size):
        print(size)
        self.text_size = size


    def read_settings(self):
        import setting
        return [setting.dark_mode, setting.save_chats, setting.wallpaper ,setting.chat_color]

    def build(self):
        self.chat_img = self.read_settings()[2]
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.theme_style = "Dark" if self.read_settings()[0] == True else "Light"
        self.chat_color = self.read_settings()[-1][0] if self.theme_cls.theme_style == "Light" else self.read_settings()[-1][-1] 
        self.theme_cls.material_style = "M3"
        self.screen_manager.add_widget(Builder.load_file("kvfiles/splash.kv"))
        self.screen_manager.current = "splash"
        return self.screen_manager

    def set_mode(self, instance):
        if instance.active == True:
            self.theme_cls.theme_style = "Dark"
            print("Hy")
        else:
            self.theme_cls.theme_style = "Light"

    def on_start(self):
        widget  = ChatText()
        widget.text  = "A long text"*20
        print(widget.ids)
        Window.bind(on_keyboard=self.handle_keys)
        Clock.schedule_once(self.load_files, 2)

    def dialog_constructor(self, message, ctext, ftext, on_ok_press, on_press_cancel=None, close_on_ok=False):
        self.dialog = Builder.load_string(open("kvfiles/asset.kv", "r").read().split("~~~")[0])
        self.dialog.ids.cb.text = ctext
        self.dialog.ids.fb.text = ftext
        self.dialog.ids.la.text = message
        if close_on_ok == False:
            self.dialog.ids.fb.on_press = on_ok_press 
        return self.dialog

    def handle_keys(self, *largs):
        key = largs[-4]
        if key == self.back_key:
            if self.screen_manager.get_screen("main").ids.drawer.pos_hint == {"center_x": 0.5, "center_y": 0.5}:
                self.open_drawer()
            else:
                self.dialog_constructor("Do you want to exit?", "Cancel", "Exit", self.stop).open()

    def load_files(self, *largs):
        self.main_screen = Builder.load_file("main.kv")
        self.chat_view = Builder.load_file("kvfiles/chat_connect.kv")
        self.server_view = Builder.load_file("kvfiles/server_start.kv")
        self.settings_view = Builder.load_file("kvfiles/settings_view.kv")
        self.chat = Builder.load_file("kvfiles/chat.kv")
        self.wall_change = Builder.load_file("kvfiles/wall.kv")
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.transition = FadeTransition()
        self.screen_manager.current = "main"
        self.screen_manager.transition = SlideTransition()

    def animate_icon(self, instance, icon, *largs):
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

    def animate_pos_hint(self, instance, pos_hint, md_bg_color=None, radius=None):
        anim = Animation(
            md_bg_color=md_bg_color,
            pos_hint=pos_hint,
            radius=radius,
            d=0.3
        )
        anim.start(instance)

    def animate_md_bg_color(self, instance, md_bg_color=None):
        anim = Animation(
            md_bg_color=md_bg_color,
            d=0.3
        )
        anim.start(instance)

    def open_modal(self, instance):
        anim = Animation(
            opacity=1,
            d=0.3
        ).start(instance)

    def close_modal(self, instance):
        anim = Animation(
            opacity=0,
            d=0.3
        ).start(instance)

    def open_drawer(self, *largs):
        animation_open = Animation(
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            d=0.3
        )
        animation_close = Animation(
            pos_hint={"center_x": -0.5, "center_y": 0.5},
            d=0.3
        )
        if self.screen_manager.get_screen("main").ids.drawer.pos_hint == {"center_x": -0.5, "center_y": 0.5}:
            animation_open.start(self.screen_manager.get_screen("main").ids.drawer)

            def set_opacity(*largs):
                self.screen_manager.get_screen("main").ids.drawer.md_bg_color = 0, 0, 0, .3

            animation_open.bind(on_complete=set_opacity)
        else:
            self.screen_manager.get_screen("main").ids.drawer.md_bg_color = 0, 0, 0, 0
            animation_close.start(self.screen_manager.get_screen("main").ids.drawer)
            Clock.schedule_once(partial(self.animate_icon, self.screen_manager.get_screen("main").ids.back_button,
                                        "menu" if self.icon == "arrow-left" else "menu"), 0.1)

    def change_size_keyboard(self, instance , key):
        try:
            from android import get_keyboard_height
            keyboard_height = lambda: get_keyboard_height()
        except Exception  as e:
            keyboard_height = lambda: 0
        if key.focus == True:
            anim = Animation(
                size=[self.x(), self.y() - keyboard_height()],
                d=0.2
            )
            anim.start(instance)
        else:
            anim = Animation(
                size=[self.x(), self.y()],
                d=0.2
            )
            anim.start(instance)

    def connect_client(self, addr, nickname, *largs):
        self.chat = Builder.load_file("kvfiles/chat.kv")
        self.nickname = nickname
        send_message = lambda: Clock.schedule_once(self.handle_chat)
        recieve_message = lambda msg, nickname: Clock.schedule_once(partial(self.handle_msg, msg, nickname))
        def shutdown(text):
            self.dialog_constructor("Error : " + text, "", "OK", self.chat.dismiss, close_on_ok=True).open()
        def close_view():
            Clock.schedule_once(self.chat.dismiss)
        try:
            self.client = appServer.handle_client(nickname, send_message, recieve_message, int(addr.split(":")[-1]),addr.split(":")[0], shutdown, close_view)
            _thread.start_new_thread(self.client[-1], ())
            self.chat.open()
        except Exception  as e:
            shutdown(str(e))
            close_view()

    def handle_chat(self, *largs):
        if self.chat.ids.text_feild.text != len(self.chat.ids.text_feild.text) * " " and len(
                self.chat.ids.text_feild.text) < self.chat_length:
            widget = ChatText()
            widget.text = self.chat.ids.text_feild.text
            print(self.chat.ids.chat_handler.add_widget(widget))
            def fix(*largs):
                self.chat.ids.text_feild.text = " "
                self.chat.ids.text_feild.focus = True
                print("on func"+str(self.text_size))
                self.chat.ids.view.scroll_to(widget)
                widget.size = [self.text_size[0],self.text_size[1]+dp(40)]
                widget.children[0].size = [self.text_size[0],self.text_size[1]+dp(40)]

            Clock.schedule_once(fix,0.01)
            return True

    def handle_msg(self, msg, nickname, *largs):
        print(msg, nickname)
        widget = PersonText()
        widget.text = msg
        widget.nickname = nickname
        self.chat.ids.chat_handler.add_widget(widget)
        self.chat.ids.view.scroll_to(widget)
        def fix(*largs):
            widget.size = [self.text_size[0],self.text_size[1]+dp(40)]
            widget.children[0].size = [self.text_size[0],self.text_size[1]+dp(40)]
    
        Clock.schedule_once(fix,0.01)
    def add_server_log(self, log):
        def add(*largs):
            label = Builder.load_string(open("kvfiles/asset.kv", "r").read().split("~~~")[-1])
            label.text = "["+self.date()+"] : "+log
            self.main_screen.ids.server_loger.add_widget(label)

        Clock.schedule_once(add)

    def start_server(self, port):
        try:
            self.main_screen.ids.server_card.opacity = 1
            _thread.start_new_thread(appServer.start_server, (int(port.text), self.add_server_log, self.stop_server))
            self.server_view.dismiss()
            self.server_running = True
            self.animate_icon(self.main_screen.ids.server_icon, "close")
            self.main_screen.ids.server_text.text = "Stop server"
            Toast("Server started successfully")
        except Exception as e:
            Toast("Unable to start server :" + str(e))
            self.server_view.dismiss()
            port.text = ""

    def stop_server(self):
        self.dialog_constructor("Shutdown requires restart","Cancel","SHUTDOWN",self.stop).open()

        # self.animate_icon(self.main_screen.ids.server_icon,"plus")
        # self.main_screen.ids.server_text.text  = "Start a server"
        # self.server_running = False
        # self.main_screen.ids.server_card.opacity  = 0
        # self.server_view.ids.test_text_feild.text = ""


PrivaChat().run()
