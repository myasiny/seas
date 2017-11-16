from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from login import *

with open("design/main.txt", "r") as pgSplash:
    Builder.load_string(pgSplash.read())

class PgLogin(Screen):
    loadString()

class PgSplash(Screen):
    def skip(self, dt):
        screen.switch_to(pages[1])

    def anim(self, dt):
        Clock.schedule_once(self.skip, 2.5)

        anim_shortname = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_shortname.start(self.txt_shortname)

        anim_longname = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_longname.start(self.txt_longname)

    def on_enter(self, *args):
        Clock.schedule_once(self.anim, 2.5)

        self.txt_shortname = self.ids["txt_shortname"]
        self.txt_shortname.opacity = 0

        self.txt_longname = self.ids["txt_longname"]
        self.txt_longname.opacity = 0

        txt_developer = self.ids["txt_developer"]
        txt_developer.opacity = 0
        anim_developer = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_developer.start(txt_developer)

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(PgSplash(name="PgSplash"))

pages = [PgSplash(name="PgSplash"),
         PgLogin(name="PgLogin")]

class SeasApp(App):
    def build(self):
        screen.current = "PgSplash"
        return screen

if __name__ == "__main__":
    Window.fullscreen = "auto"
    SeasApp().run()