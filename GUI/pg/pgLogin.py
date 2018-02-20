from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

import sys
sys.path.append("../..")

from functools import partial
from Server import DatabaseAPI
from GUI.func.check_connection import check_connection

def load_string(name):
    with open("css/%s.seas" % name, "r") as design:
        Builder.load_string(design.read())

def on_enter(self):
    Clock.schedule_once(partial(check_connection, self.ids["img_connection"]))

def on_login(self, pages, screen):
    btn_login = self.ids["btn_login"]
    btn_login.disabled = True

    img_status = self.ids["img_status"]
    img_status.source = "img/ico_loading.gif"
    img_status.opacity = 0
    img_status.reload()

    anim_status = Animation(opacity=1, duration=1)
    anim_status.start(img_status)

    input_username = self.ids["input_username"].text
    input_password = self.ids["input_password"].text
    if input_username == "" or input_password == "":
        anim_status.stop(img_status)

        img_status.source = "img/ico_warning.png"
        img_status.opacity = 1
        img_status.reload()

        btn_login.disabled = False
    else:
        try:
            # data = DatabaseAPI.signIn("http://10.50.81.24:8888", "istanbul sehir university", input_username, input_password)
            data = ["TODO", "TODO", "TODO", "TODO", "TODO", "TODO", "TODO", "TODO"]
        except:
            data = None
            print ("SEAS [ERROR]: pgLogin > Except > Server Communication Failed")

        if isinstance(data, list):
            anim_status.stop(img_status)

            img_status.source = "img/ico_success.png"
            img_status.opacity = 1
            img_status.reload()

            btn_login.disabled = False

            with open("data/temp_login.seas", "w+") as temp_login:
                for d in data:
                    temp_login.write(str(d) + "\n")
                temp_login.close()

            # if role != "student":
            #     pages.append(PgLects(name="PgLects"))
            # else:
            #     pages.append(PgLects(name="PgLects"))

            try:
                screen.switch_to(pages[2])
            except:
                screen.current = pages[2].name
        else:
            anim_status.stop(img_status)

            img_status.source = "img/ico_fail.png"
            img_status.opacity = 1
            img_status.reload()

            btn_login.disabled = False

    del pages[1]

def on_quit(self):
    popup_content = FloatLayout()
    popup = Popup(title="Quit",
                  content=popup_content, separator_color=[140 / 255., 55 / 255., 95 / 255., 1.],
                  size_hint=(None, None), size=(self.width / 5, self.height / 5))
    popup_content.add_widget(Image(source="img/widget_75_gray.png", allow_stretch=True, keep_ratio=False,
                                   size=(self.width, self.height), pos_hint={"center_x":.5, "center_y":.5}))
    popup_content.add_widget(Label(text="Are you sure?", color=(0,0,0,1),
                                   font_name="font/CaviarDreams.ttf", font_size=self.width / 50,
                                   pos_hint={"center_x": .5, "center_y": .6}))
    popup_content.add_widget(Button(text="Yes",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_green.png",
                                    background_down="img/widget_100_green_selected.png",
                                    size_hint_x=None, width=self.width/ 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .25, "y": .01},
                                    on_release=App.get_running_app().stop))
    popup_content.add_widget(Button(text="No",
                                    font_name="font/LibelSuit.ttf",
                                    font_size=self.height / 40,
                                    background_normal="img/widget_100_red.png",
                                    background_down="img/widget_100_red_selected.png",
                                    size_hint_x=None, width=self.width/ 11,
                                    size_hint_y=None, height=self.height / 25,
                                    pos_hint={"center_x": .75, "y": .01},
                                    on_release=popup.dismiss))
    popup.open()