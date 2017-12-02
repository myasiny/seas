from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from functools import partial
from GUI.func.date_time import date_time
from GUI.func.check_connection import check_connection

def load_string():
    with open("css/educator.seas", "r") as design:
        Builder.load_string(design.read())

def on_quit():
    App.get_running_app().stop()

def on_logout(pages, screen):
    screen.current = pages[1].name

def on_enter(self):
    Clock.schedule_interval(partial(date_time, self.ids["txt_clock"]), 1.0)
    Clock.schedule_interval(partial(check_connection, self.ids["img_connection"]), 1.0/60.0)