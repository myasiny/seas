from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation

from functools import partial
from GUI.func.check_connection import check_connection

def load_string():
    with open("css/login.seas", "r") as design:
        Builder.load_string(design.read())

def on_quit():
    App.get_running_app().stop()

def on_enter(self):
    Clock.schedule_interval(partial(check_connection, self.ids["img_connection"]), 1.0/60.0)

def on_login(self, pages, screen):
    btn_login = self.ids["btn_login"]
    btn_login.disabled = True

    img_status = self.ids["img_status"]
    img_status.source = "img/ico_connect.png"
    img_status.reload()

    anim_status = Animation(x=img_status.x+5, opacity=1, duration=1) + Animation(x=img_status.x-5, opacity=0, duration=1)
    anim_status.repeat = True
    anim_status.start(img_status)

    input_username = self.ids["input_username"].text
    input_password = self.ids["input_password"].text
    if input_username == "" or input_password == "":
        anim_status.stop(img_status)

        img_status.source = "img/ico_warning.png"
        img_status.reload()

        btn_login.disabled = False
    elif input_username == "admin" and input_password == "123":
        anim_status.stop(img_status)

        img_status.source = "img/ico_success.png"
        img_status.reload()

        screen.switch_to(pages[2])
    else:
        pass # TODO: Add User Login Through Server