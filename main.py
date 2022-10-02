from kivy.lang import Builder
from kivy.uix.behaviors import TouchRippleBehavior
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import *
from kivymd.uix.templates import RotateWidget
from kivymd.uix.button import *
from kivymd.uix.dialog import MDDialog
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.toast import toast as Toast2
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivy.metrics import dp,sp
from kivy.utils import *
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.config import Config
from datetime import datetime
from kivy.uix.screenmanager import *
from gestures4kivy.commongestures import CommonGestures
from kivy_garden.frostedglass import FrostedGlass
import _thread
import appServer
import os

__version__ = "1.0"

if platform != "android":
    Config.set("graphics", "height", "700")
    Config.set("graphics", "width", "400")
    Config.set("graphics", "fps", "120")
    from kivy.core.window import Window
    Window.size = [dp(400), dp(700)]

Config.set("kivy", "exit_on_escape", "0")


class IconButton(MDIconButton, RotateBehavior):
    pass


class ChatText(MDRelativeLayout):
    pass


class PersonText(MDRelativeLayout):
    pass


class HoverLayout(MDCard, HoverBehavior):
    pass


class MDCustomCard(
    DeclarativeBehavior,
    ThemableBehavior,
    BackgroundColorBehavior,
    TouchBehavior,
    focus_behavior.FocusBehavior,
    BoxLayout
    ):

    focus_behavior = BooleanProperty(False)
    ripple_behavior = BooleanProperty(False)
    elevation = 0
    shadow_softness = 0
    style = "filled"
    #radius = [dp(10),dp(10),dp(10),dp(10)]
    #md_bg_color = get_color_from_hex("#1D2227")
    name = "none"

    def on_double_tap(self, touch, *args):
        if self.name == "chatcard":
            Animation(opacity=0,d=0.3).start(self.parent)

class MDScreenG(MDScreen,CommonGestures):

    def cg_swipe_horizontal(*largs):

        app = MDApp.get_running_app()

        if largs[-1] == True:
            if largs[0].name == "chat":
                app.open_drawer()
            if largs[0].name == "server":
                app.animate_pos_hint(app.screen_manager.get_screen("main").ids.card,app.screen_manager.get_screen("main").ids.cc.pos_hint,md_bg_color=app.theme_cls.primary_dark,radius=[dp(10),0,0,dp(10)])
                app.screen_manager.get_screen("main").ids.tab_manager.transition.direction = "right"
                app.screen_manager.get_screen("main").ids.tab_manager.current = "chat"
        else:
             if largs[0].name == "chat":
                app.animate_pos_hint(app.screen_manager.get_screen("main").ids.card,app.screen_manager.get_screen("main").ids.sc.pos_hint,md_bg_color=app.theme_cls.accent_dark,radius=[0,dp(10),dp(10),0])
                app.screen_manager.get_screen("main").ids.tab_manager.transition.direction = "left"
                app.screen_manager.get_screen("main").ids.tab_manager.current = "server"


class ImgBox(MDCard):
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
    theme_change = None
    dialog = MDDialog

    ChatText = ChatText
    Toast = lambda self,text : Toast(text)

    date = lambda self: datetime.now().strftime("%H:%M:%S")
    nickname = ""
    chat_length = 1000
    text_size = None

    title = "PrivaChat (Running)"
    icon = "splash.png"

    back_key = 27

    MDLabel = MDLabel

    colors =  {
        "Red":  "#F44336", 
        "Pink": "#E91E63", 
        "Purple":"#9C27B0", 
        "DeepPurple":"#673AB7", 
        "Indigo":"#3F51B5",
        "Blue":"#2196F3", 
        "LightBlue":"#03A9F4", 
        "Cyan":"#00BCD4", 
        "Teal":"#009688",
        "Green":"#4CAF50", 
        "LightGreen":"#8BC34A", 
        "Lime":"#CDDC39", 
        "Yellow":"#FFEB3B", 
        "Amber":"#FFC107", 
        "Orange":"#FF9800", 
        "DeepOrange":"#FF5722", 
        "Brown":"#795548", 
        "Gray":"#9E9E9E", 
        "BlueGray":"#607D8B"
                }

    def open_wall(self):
        self.wall_change.open()

    def open_theme(self):
        #for i in self.colors.keys():

        self.theme_change.open()

    def ch_s(self,size):
        self.text_size = size


    def read_settings(self):
        import setting
        return [
                setting.dark_mode,
                setting.save_chats,
                setting.wallpaper,
                setting.chat_color,
                setting.wallpaper_path,
                setting.accent_palette,
                setting.primary_palette,
                setting.lock_pass
                ]

    def write_settings(self,key,value):
        file = open("setting.py","r")
        read = file.read().split("\n")
        for count,line in enumerate(read):
            if line.split(" ")[0] == key:
                read[count] = key+" = "+value
                open("setting.py","w").write("\n".join(read))

    def build(self):
        self.lock_pass = self.read_settings()[7]
        self.chat_img = self.read_settings()[2]
        self.theme_cls.accent_palette = self.read_settings()[5]
        self.theme_cls.primary_palette = self.read_settings()[6]
        self.theme_cls.theme_style = "Dark" 
        self.chat_color = self.read_settings()[3]
        self.theme_cls.material_style = "M3"
        self.screen_manager.add_widget(Builder.load_file("kvfiles/splash.kv"))
        self.screen_manager.current = "splash"
        return self.screen_manager

    def set_mode(self, instance):
        if instance.active == True:
            self.write_settings("dark_mode","True")
            self.write_settings("chat_color",'"#162D3E"')
            self.theme_cls.theme_style = "Dark"
            self.chat_color =  "#162D3E"
            self.chat_img = "wallpapers/planet.jpg"
            self.chat_view = Builder.load_file("kvfiles/chat_connect.kv")
            self.server_view = Builder.load_file("kvfiles/server_start.kv")

        else:
            self.write_settings("dark_mode","False")
            self.write_settings("chat_color",'"#FCEFBA"')
            self.theme_cls.theme_style = "Light"
            self.chat_color = "#FCEFBA"
            self.chat_img = "wallpapers/mountains.png"
            self.chat_view = Builder.load_file("kvfiles/chat_connect.kv")
            self.server_view = Builder.load_file("kvfiles/server_start.kv")
            self.startup = Builder.load_file("kvfiles/startup.kv")

    def on_start(self):
        Window.bind(on_keyboard=self.handle_keys)
        Clock.schedule_once(self.load_files,1)
        Clock.schedule_once(self.add_images,0.5)

    def add_images(self,arg):
        self.root.opacity = 0 
        for dir in self.read_settings()[4]:
            try:
                if os.path.isdir(dir):
                    for file in os.listdir(dir):
                        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                            widget = ImgBox()
                            img_file = dir+"/"+file
                            widget.img = img_file 
                            if img_file == self.chat_img:
                                widget.style = "outlined"
                            self.wall_change.ids.wall_box.add_widget(widget)
            except Exception as e:
                pass         
        self.root.opacity = 1
        

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
        self.lock = Builder.load_file("kvfiles/lock.kv")
        self.wall_change = Builder.load_file("kvfiles/wall.kv")
        self.theme_change = Builder.load_file("kvfiles/theme.kv")
        self.startup = Builder.load_file("kvfiles/startup.kv")
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.lock)
        self.screen_manager.add_widget(self.startup)
        self.screen_manager.transition = FadeTransition()
        self.screen_manager.current = "lock" if self.lock_pass != None else "main"

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

    def animate_font_size(self,instance,font_size=None,ori=None,ok=False):
        anim = Animation(
            font_size=font_size,
            d=0.15
            )
        anim.start(instance)
        if ok == True:
            anim.bind(on_complete=lambda self,arg : MDApp.get_running_app().animate_font_size(instance,font_size=ori))

    def animate_icon_size(self,instance,icon_size=None,ori=None,ok=False):
        anim = Animation(
            icon_size=icon_size,
            d=0.15
            )
        anim.start(instance)
        if ok == True:
            anim.bind(on_complete=lambda self,arg : MDApp.get_running_app().animate_icon_size(instance,icon_size=ori))

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

    def handle_lock(self,text):

        ids = [self.lock.ids.l1,self.lock.ids.l2,self.lock.ids.l3,self.lock.ids.l4]
        
        for count,ido in enumerate(ids):
            if ido.to == "":
                ido.to = text
                ido.text = text
                anim = Animation(
                    font_size=sp(30),
                    d=0.1
                    ) + Animation(
                    font_size=sp(0),
                    d=0.1
                    )
                anim.start(ido)

                def f(*largs):
                    ido.text = "."
                    Animation(font_size=sp(30),d=0.1).start(ido)
                
                anim.bind(on_complete = f)


                if count == 3:
                    def pass_lock(arg):
                        lock =  [self.lock.ids.l1.to,self.lock.ids.l2.to,self.lock.ids.l3.to,self.lock.ids.l4.to]
                        if "".join(lock) == str(self.lock_pass):
                            self.theme_cls.theme_style = "Dark" if self.read_settings()[0] == True else "Light"
                            self.screen_manager.current = "main"
                        else:
                            for id in ids:
                                id.text = " "
                                id.to = ""

                            anim = Animation(
                                pos_hint = {"center_x":0.45,"center_y":0.9},
                                d=0.1
                                ) + Animation(
                                pos_hint = {"center_x":0.55,"center_y":0.9},
                                d=0.1                                
                                ) + Animation(
                                pos_hint = {"center_x":0.5,"center_y":0.9},
                                d=0.1
                                )
                            anim.start(self.lock.ids.lock_icon)
                            def more(*largs):
                                ids[3].text = " "
                                ids[3].to = ""
                            Clock.schedule_once(more,0.35)
                    Clock.schedule_once(pass_lock,0.5)


                    break
                else:
                    break

    def fix_width(self,instance):
        for widget in self.wall_change.ids.wall_box.children:
            if widget != instance:
                widget.line_color = (0,0,0,0)
            else:
                widget.line_color =  self.theme_cls.primary_color

    def erase_message_lock(self):
        ids = [self.lock.ids.l1,self.lock.ids.l2,self.lock.ids.l3,self.lock.ids.l4]
        
        for count,ido in enumerate(ids[::-1]):
            if ido.text == ".":
                ido.text = " "
                ido.to  = ""
                break

    def lock_screen(self):
        ids = [self.lock.ids.l1,self.lock.ids.l2,self.lock.ids.l3,self.lock.ids.l4]
        for wi in ids:
            wi.text = " "
            wi.to = ""
        self.screen_manager.current = "lock"

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
            Clock.schedule_once(
                partial(
                    self.animate_icon, 
                        self.screen_manager.get_screen("main").ids.back_button,
                        "menu" if self.icon == "arrow-left" else "menu"), 
            0.1)

    def change_size_keyboard(self):
        try:
            from android import get_keyboard_height
            keyboard_height = lambda: get_keyboard_height() + dp(20)

        except Exception  as e:
            keyboard_height = lambda: 0
        if self.chat.ids.text_feild.focus == True:
        	anim = Animation(
        		size=[self.x(),self.y()-keyboard_height()],
        		d=0.2
        	)
        	anim.start(self.chat.ids.main_handler)
        	def fix(*largs):
        		self.chat.ids.main_handler.size = [self.x(),self.y()-keyboard_height()]
        	anim.bind(on_complete=fix)
        		
        		
        else:
        	anim = Animation(
        		size=[self.x(),self.y()],
        		d=0.2
        	)
        	anim.start(self.chat.ids.main_handler)        	

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
            self.chat.ids.chat_handler.add_widget(widget)
            def fix(*largs):
                self.chat.ids.text_feild.text = ""
                self.chat.ids.view.scroll_to(widget)
                widget.size = [self.text_size[0],self.text_size[1]+dp(40)]
                widget.children[0].size = [self.text_size[0],self.text_size[1]+dp(40)]

            Clock.schedule_once(fix,0.01)
            return True

    def handle_msg(self, msg, nickname, *largs):
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
            self.main_screen.ids.addr_box.opacity = 1
            self.main_screen.ids.addr_text.text = "127.0.0.1:"+port.text
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


PrivaChat().run()
