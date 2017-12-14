from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation

import sys
sys.path.append("../..")

from Server import DatabaseAPI
from functools import partial
from GUI.func.date_time import date_time
from GUI.func.check_connection import check_connection

def load_string(name):
    with open("css/" + name + ".seas", "r") as design:
        Builder.load_string(design.read())

def on_quit():
    App.get_running_app().stop()

def on_enter(self):
    Clock.schedule_interval(partial(date_time, self.ids["txt_clock"]), 1.0)
    Clock.schedule_once(partial(check_connection, self.ids["img_connection"]))

def on_login(self, pages, screen):
    btn_login = self.ids["btn_login"]
    btn_login.disabled = True

    img_status = self.ids["img_status"]
    img_status.source = "img/ico_connect.png"
    img_status.opacity = 0
    img_status.reload()

    anim_status = Animation(x=img_status.x+5, opacity=1, duration=1) + Animation(x=img_status.x-5, opacity=0, duration=1)
    anim_status.repeat = True
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
            #data = ["LOCAL TEST","DELETE","LOCAL TEST","DELETE","LOCAL TEST","DELETE","LOCAL TEST","DELETE"]
            data = DatabaseAPI.signIn("http://10.50.81.24:8888", "istanbul sehir university", input_username, input_password)
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

def on_check_connection(self):
    Clock.schedule_once(partial(check_connection, self.ids["img_connection"]))