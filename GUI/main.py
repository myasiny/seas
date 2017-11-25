from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin

with open("css/main.seas", "r") as pgSplash:
    Builder.load_string(pgSplash.read())

class PgLogin(Screen):
    pgLogin.load_string()

    def on_quit(self):
        pgLogin.on_quit(self)

    def on_login(self):
        pgLogin.on_login(self)

class PgSplash(Screen):
    def skip(self, dt):
        screen.switch_to(pages[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 2)

        txt_shortname = self.ids["txt_shortname"]
        txt_shortname.opacity = 0
        anim_shortname = Animation(y=self.y+25, opacity=1, duration=1) + Animation(y=self.y-25, opacity=0, duration=1)
        anim_shortname.start(txt_shortname)

        txt_longname = self.ids["txt_longname"]
        txt_longname.opacity = 0
        anim_longname = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        anim_longname.start(txt_longname)

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