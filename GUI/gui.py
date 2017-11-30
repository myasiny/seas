from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pg import pgLogin, pgEducator

class Tab_Two(Screen):
    pass

class Tab_One(Screen):
    pass

class PgEducator(Screen):
    pgEducator.load_string()

    def on_quit(self):
        pgLogin.on_quit()

    def on_enter(self, *args):
        pgLogin.on_enter(self)

class PgLogin(Screen):
    pgLogin.load_string()

    def on_quit(self):
        pgLogin.on_quit()

    def on_enter(self, *args):
        pgLogin.on_enter(self)

    def on_login(self):
        pgLogin.on_login(self, pages, screen)

with open("css/splash.seas", "r") as design:
    Builder.load_string(design.read())

class PgSplash(Screen):
    def skip(self, dt):
        screen.switch_to(pages[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 1)

        txt_shortname = self.ids["txt_shortname"]
        txt_shortname.opacity = 0

        txt_longname = self.ids["txt_longname"]
        txt_longname.opacity = 0

        anim_fade = Animation(opacity=1, duration=0.5) + Animation(opacity=0, duration=0.5)
        anim_fade.start(txt_shortname)
        anim_fade.start(txt_longname)

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(PgSplash(name="PgSplash"))

pages = [PgSplash(name="PgSplash"),
         PgLogin(name="PgLogin"),
         PgEducator(name="PgEducator")]

class SeasApp(App):
    def build(self):
        screen.current = "PgSplash"
        return screen

if __name__ == "__main__":
    Window.fullscreen = "auto"
    SeasApp().run()