from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from functools import partial
from GUI.func.check_connection import check_connection

def load_string():
    with open("css/educator.seas", "r") as design:
        Builder.load_string(design.read())

def on_quit():
    App.get_running_app().stop()

def on_enter(self):
    Clock.schedule_interval(partial(check_connection, self.ids["img_connection"]), 1.0/60.0)